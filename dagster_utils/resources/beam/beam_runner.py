from typing import Any, Protocol, Optional


class BeamRunner(Protocol):
    def run(
            self,
            run_arg_dict: dict[str, Any],
            target_class: str,
            scala_project: str,
            job_name: Optional[str] = None,
            command: Optional[list[str]] = None
    ) -> None:
        ...
