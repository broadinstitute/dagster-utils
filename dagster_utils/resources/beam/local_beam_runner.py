import subprocess
from dataclasses import dataclass
from typing import Any, Optional

from dagster import DagsterLogManager, resource, Field, StringSource
from dagster.core.execution.context.init import InitResourceContext

from dagster_utils.resources.beam.beam_runner import BeamRunner


@dataclass
class LocalBeamRunner(BeamRunner):
    working_dir: str
    logger: DagsterLogManager

    def __post_init__(self) -> None:
        self.arg_dict = {
            "runner": "direct",
        }

    def run(
            self,
            run_arg_dict: dict[str, Any],
            target_class: str,
            scala_project: str,
            job_name: Optional[str] = None
    ) -> None:
        # create a new dictionary containing the keys and values of arg_dict + solid arguments
        local_run_flags = {**self.arg_dict, **run_arg_dict}
        self.logger.info("Local beam runner")

        # list comprehension over args_dict to get flags
        flags = " ".join([f'--{arg}={value}' for arg, value in local_run_flags.items()])
        subprocess.run(
            ["sbt", f'{scala_project}/runMain {target_class} {flags}'],
            check=True,
            cwd=self.working_dir
        )


@resource({
    "working_dir": Field(StringSource),
})
def local_beam_runner(init_context: InitResourceContext) -> LocalBeamRunner:
    return LocalBeamRunner(
        working_dir=init_context.resource_config["working_dir"],
        logger=init_context.log_manager
    )
