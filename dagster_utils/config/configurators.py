import os
from typing import Optional, Protocol

from dagster import configured, Noneable
from dagster.core.definitions.configurable import ConfigurableDefinition

from dagster_utils.typing import DagsterConfigDict, DagsterObjectConfigSchema, LocatablePackage
from dagster_utils.config.preconfiguration_loader import PreconfigurationLoader


class PreconfiguratorFunction(Protocol):
    def __call__(
        self,
        dagster_object: ConfigurableDefinition,
        mode_name: str,
        additional_schema: DagsterObjectConfigSchema = {},
        subdirectory: Optional[str] = None,
    ) -> ConfigurableDefinition: ...


def configurator_aimed_at(
    package: LocatablePackage,
) -> PreconfiguratorFunction:
    return configurator_aimed_at_directory(os.path.dirname(package.__file__))


def configurator_aimed_at_directory(
    package_directory: str,
) -> PreconfiguratorFunction:
    """
    Generates a configuration function that loads config from YAML within the specified package directory.
    See the inner function for details on how it works.

    Example usage:
    preconfigure_for_mode = configurator_aimed_at(os.path.dirname(my_dagster_project.config.__file__))

    preconfigure_for_mode(some_resource, "dev") # => configuration pulled from [package_root]/my_dagster_project/config/some_resource/
    """

    def preconfigure_for_mode(
        dagster_object: ConfigurableDefinition,
        mode_name: str,
        additional_schema: DagsterObjectConfigSchema = {},
        subdirectory: Optional[str] = None,
    ) -> ConfigurableDefinition:
        """
        Preconfigures a Dagster object (such as a resource) for a given mode by setting all config values
        for the object to values found in the config files in the specified directory.

        The method will load from the specified directory under [base_config_package_dir]/config/, looking for:
        * global.yaml
        * [mode_name].yaml

        Values in the mode-specific config wil supersede global config. Only one of these needs to be present.

        This method expects a value to be specified for all required fields in the object's config schema. If
        a value should remain configurable after preconfiguration, list it in the `additional_schema` argument.
        If any values it expects to be specified are missing, it will raise an error. If any values for
        fields it does not expect are specified, it will record a warning and ignore those values.

        If a config field is optional (i.e. it has the Noneable type), it does not need to be configured in the YAML,
        but it will be unconfigurable in the resulting solid unless it is listed in additional_schema.

        :param dagster_object: The definition for the object to be configured (e.g. a ResourceDefinition).
        :param mode_name: The name of the mode. This will determine the name of the mode-specific config file to load.
        :param additional_schema: Any config schema that is part of the Dagster object but should NOT be preconfigured.
        :param subdirectory: Which directory to search for the config files. Defaults to the name of the Dagster object
            beneath your_repo_name_here.config.
        :return: The Dagster object configured with the loaded values.
        """

        # [NOTE]
        # This line assumes the Dagster object is configured with a dict. Other dagster config patterns,
        # such as a single primitive type, aren't accounted for (but probably shouldn't be used,
        # since they provide no context for the config setting's meaning/purpose)
        definition_config_keys = dagster_object.config_schema.config_type.fields
        optional_config_keys = [k for k, v in definition_config_keys.items() if isinstance(v.config_type, Noneable)]
        required_config_keys = [k for k, v in definition_config_keys.items() if k not in optional_config_keys]
        subdirectory = subdirectory or dagster_object.__name__
        config_file_directory = os.path.join(package_directory, subdirectory)
        loader = PreconfigurationLoader(
            name=dagster_object.__name__,
            config_file_directory=config_file_directory,
            required_keys=(set(required_config_keys) - set(additional_schema.keys())),
            optional_keys=(set(optional_config_keys) - set(additional_schema.keys()))
        )

        # we load the config in preconfigure_for_mode instead of in the @configured function to
        # ensure that any config issues cause errors upon initialization, instead of waiting until
        # we try to use the object being configured
        loaded_config = loader.load_for_mode(mode_name)

        @configured(dagster_object, additional_schema)
        def __dagster_object_preconfigured(extra_config: DagsterConfigDict) -> DagsterConfigDict:
            return {
                **loaded_config,
                **extra_config,
            }

        return __dagster_object_preconfigured

    return preconfigure_for_mode
