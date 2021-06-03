from typing import Any, Protocol


class BeamRunner(Protocol):
    def run(self, run_arg_dict: dict[str, Any], target_class: str, scala_project: str) -> None:
        ...
