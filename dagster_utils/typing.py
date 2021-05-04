"""
Types and type annotations useful for Dagster applications.
"""

from dagster import HookContext, InputDefinition
from dagster.config import ConfigType as DagsterConfigType

from typing import Callable, Literal, Protocol, TypedDict, Union


# dict of config settings for a given instance of a dagster object
# assumes the config is flat (i.e. only primitive types)
DagsterConfigDict = dict[
    str,
    Union[
        dict[
            Literal['env'],
            str
        ],
        str,
        int,
        float,
        bool
    ]
]

# dict representing how a solid can be configured
DagsterObjectConfigSchema = dict[str, DagsterConfigType]

DagsterHookFunction = Callable[[HookContext], None]


# a partial delineation of the config for a Dagster solid.
class DagsterSolidConfig(TypedDict, total=False):
    required_resource_keys: set[str]
    input_defs: list[InputDefinition]
    config_schema: DagsterObjectConfigSchema


# a package whose location on the filesystem is fetchable
class LocatablePackage(Protocol):
    @property
    def __file__(self) -> str: ...
