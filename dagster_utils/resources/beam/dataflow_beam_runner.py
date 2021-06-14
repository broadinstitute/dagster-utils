from typing import Any, Optional
from dataclasses import dataclass
import subprocess

from dagster import DagsterLogManager, resource, Field, IntSource, StringSource
from dagster.core.execution.context.init import InitResourceContext

from dagster_utils.resources.beam.beam_runner import BeamRunner


@dataclass
class DataflowBeamRunner(BeamRunner):
    working_dir: str
    logger: DagsterLogManager
    region: str
    worker_machine_type: str
    autoscaling_algorithm: str
    num_workers: int
    max_num_workers: int
    google_project: str

    def __post_init__(self) -> None:
        self.arg_dict = {
            "region": self.region,
            "workerMachineType": self.worker_machine_type,
            "autoscalingAlgorithm": self.autoscaling_algorithm,
            "numWorkers": str(self.num_workers),
            "maxNumWorkers": str(self.max_num_workers),
            "project": self.google_project,
            # specific to dataflow runner
            "runner": "dataflow",
            "experiments": "shuffle_mode=service",
        }

    def run(
            self,
            run_arg_dict: dict[str, Any],
            target_class: str,
            scala_project: str,
            job_name: Optional[str] = None
    ) -> None:
        # create a new dictionary containing the keys and values of arg_dict + solid arguments
        dataflow_run_flags = {**self.arg_dict, **run_arg_dict}
        self.logger.info("Dataflow beam runner")

        # list comprehension over args_dict to get flags
        flags = " ".join([f'--{arg}={value}' for arg, value in dataflow_run_flags.items()])
        subprocess.run(
            ["sbt", f'{scala_project}/runMain {target_class} {flags}'],
            check=True,
            cwd=self.working_dir
        )


@resource({
    "working_dir": Field(StringSource),
    "region": Field(StringSource),
    "worker_machine_type": Field(StringSource),
    "autoscaling_algorithm": Field(StringSource),
    "num_workers": Field(IntSource),
    "max_num_workers": Field(IntSource),
    "google_project": Field(StringSource),
})
def dataflow_beam_runner(init_context: InitResourceContext) -> DataflowBeamRunner:
    return DataflowBeamRunner(
        working_dir=init_context.resource_config["working_dir"],
        region=init_context.resource_config["region"],
        worker_machine_type=init_context.resource_config["worker_machine_type"],
        autoscaling_algorithm=init_context.resource_config["autoscaling_algorithm"],
        num_workers=init_context.resource_config["num_workers"],
        max_num_workers=init_context.resource_config["max_num_workers"],
        google_project=init_context.resource_config["google_project"],
        logger=init_context.log_manager,
    )
