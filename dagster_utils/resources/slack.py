from dataclasses import dataclass
from typing import Callable, Literal, Optional

import slack
from dagster import DagsterLogManager, failure_hook, HookContext, HookDefinition,\
    resource, String, StringSource, success_hook
from dagster.core.execution.context.init import InitResourceContext

from dagster_utils.typing import DagsterHookFunction

SlackMessageGenerator = Callable[[HookContext], str]


@dataclass
class ConsoleSlackClient:
    logger: DagsterLogManager

    def send_message(self, text: Optional[str] = None, blocks: Optional[list[dict[str, object]]] = None) -> None:
        self.logger.info(f"[SLACK] {text} {blocks}")


@resource
def console_slack_client(init_context: InitResourceContext) -> ConsoleSlackClient:
    return ConsoleSlackClient(init_context.log)


@dataclass
class LiveSlackClient:
    client: slack.WebClient
    channel: str

    def send_message(self, text: Optional[str] = None, blocks: Optional[list[dict[str, object]]] = None) -> None:
        self.client.chat_postMessage(channel=self.channel, text=text, blocks=blocks)


@resource({
    'channel': String,
    'token': StringSource,
})
def live_slack_client(init_context: InitResourceContext) -> LiveSlackClient:
    return LiveSlackClient(
        slack.WebClient(init_context.resource_config['token']),
        init_context.resource_config['channel'],
    )


def slack_hook(
    on: Literal['success', 'failure'],
    additional_resource_keys: set[str] = set()
) -> Callable[[SlackMessageGenerator], DagsterHookFunction]:
    """
    Decorator function for Slack hooks - decorate a function that generates a message to turn it
    into a boilerplate Slack hook you can bind to solids/pipelines. Presumes that the Slack resource
    is already fully configured with its target channel and token.

    Example usage (real world example):
        @slack_hook(on='success', additional_resource_keys={'ornithologist'})
        def do_owls_exist(context: HookContext) -> str:
            if context.resources.ornithologist.are_there_owls():
                return "heck yeah"

            return "no owls in this world"

        # then you can call:
        create_world_with_potential_for_owls.with_hooks({do_owls_exist})()
    """

    if on == 'success':
        hook_decorator = success_hook
    elif on == 'failure':
        hook_decorator = failure_hook

    def message_generation_wrapper(message_generator: SlackMessageGenerator) -> HookDefinition:

        @hook_decorator(required_resource_keys=({'slack'} | additional_resource_keys))
        def _send_slack_message(context: HookContext) -> None:
            context.resources.slack.send_message(message_generator(context))

        return _send_slack_message

    return message_generation_wrapper
