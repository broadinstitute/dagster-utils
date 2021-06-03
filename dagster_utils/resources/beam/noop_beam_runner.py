from typing import Any

from dagster import resource
from dagster.core.execution.context.init import InitResourceContext

from dagster_utils.resources.beam.beam_runner import BeamRunner


class NoopBeamBeamer(BeamRunner):
    def run(
            self,
            run_arg_dict: dict[str, Any],
            target_class: str,
            scala_project: str,
    ) -> None:
        pass


@resource
def noop_beam_runner(init_context: InitResourceContext) -> NoopBeamBeamer:
    return NoopBeamBeamer()
