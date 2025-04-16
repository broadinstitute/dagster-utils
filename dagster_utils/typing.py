"""
Types and type annotations useful for Dagster applications.
"""

from dagster import HookContext
from dagster.config import ConfigType as DagsterConfigType

from typing import Callable, Literal, Protocol, Union


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

# dict representing how an op can be configured
DagsterObjectConfigSchema = dict[str, DagsterConfigType]

DagsterHookFunction = Callable[[HookContext], None]


# TODO clean this up and remove the commented out code
#  - this class is not used in dagster-utils or in hca-ingest
# a partial delineation of the config for a Dagster op.
# class DagsterOpConfig(TypedDict, total=False):
#     required_resource_keys: set[str]
#     input_defs: list[In]
#     config_schema: DagsterObjectConfigSchema


# a package whose location on the filesystem is fetchable
class LocatablePackage(Protocol):
    @property
    def __file__(self) -> str: ...
