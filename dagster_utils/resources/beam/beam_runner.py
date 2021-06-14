from typing import Any, Protocol


class BeamRunner(Protocol):
    def run(self, run_arg_dict: dict[str, Any], job_name: str, target_class: str, scala_project: str) -> None:
        ...
