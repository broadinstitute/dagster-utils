from contextlib import contextmanager

from typing import Any

from dagster import DagsterInstance, ResourceDefinition
from dagster.core.execution.build_resources import build_resources
from dagster_utils.typing import DagsterConfigDict


# n.b. 2021-03-22
# dagster support for testing resources in isolation is currently in active development.
# expect this section to use more robust and unchanging tooling as it becomes available over the next few months
@contextmanager
def initialize_resource(resource_def: ResourceDefinition, config: DagsterConfigDict = {}) -> Any:
    with build_resources(
        {
            'test_resource': resource_def,
        },
        DagsterInstance.ephemeral(),
        {
            'test_resource': {
                'config': config,
            }
        }
    ) as resource_context:
        yield resource_context.test_resource
