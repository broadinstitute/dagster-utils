import os
from tempfile import TemporaryDirectory
import unittest
import yaml

import dagster as dg

import dagster_utils.config
from dagster_utils.config import configurator_aimed_at
from dagster_utils.testing.filesystem import EphemeralNamedDirectory


class ConfiguratorAimedAtTestCase(unittest.TestCase):
    def setUp(self):
        self.dummy_function = lambda _: 0
        self.dummy_function.__name__ = 'steve'
        self.config_package_dir = os.path.dirname(dagster_utils.config.__file__)
        self.configurator = configurator_aimed_at(dagster_utils.config)

    def test_treats_noneable_fields_as_optional(self):
        op_def = dg.op(config_schema={
            'a': dg.Noneable(dg.String),
            'b': dg.String,
        })(self.dummy_function)

        with TemporaryDirectory(dir=self.config_package_dir) as temp_dir:
            with open(os.path.join(temp_dir, 'mode.yaml'), 'w') as config_yaml_io:
                yaml.dump({'b': 'steve'}, config_yaml_io)

            preconfigured = self.configurator(
                op_def,
                'mode',
                subdirectory=os.path.basename(temp_dir))
            # assert that it accepts no additional config
            self.assertEqual(preconfigured.get_config_field().config_type.fields, {})

    def test_marks_non_noneable_fields_as_required(self):
        op_def = dg.op(config_schema={
            'a': dg.String,
            'b': dg.String,
        })(self.dummy_function)

        with TemporaryDirectory(dir=self.config_package_dir) as temp_dir:
            with open(os.path.join(temp_dir, 'mode.yaml'), 'w') as config_yaml_io:
                yaml.dump({'b': 'steve'}, config_yaml_io)

            with self.assertRaises(ValueError):
                self.configurator(
                    op_def,
                    'mode',
                    subdirectory=os.path.basename(temp_dir))

    def test_defaults_to_using_resource_name_for_directory(self):
        op_def = dg.op(config_schema={
            'a': dg.String,
            'b': dg.String,
        })(self.dummy_function)

        with EphemeralNamedDirectory('steve', self.config_package_dir) as temp_dir:
            with open(os.path.join(temp_dir, 'global.yaml'), 'w') as config_yaml_io:
                yaml.dump({'a': 'sneve', 'b': 'steve'}, config_yaml_io)

            preconfigured = self.configurator(op_def, 'mode')
            # assert that it accepts no additional config
            self.assertEqual(preconfigured.get_config_field().config_type.fields, {})

    def test_doesnt_require_fields_in_additional_schema(self):
        op_def = dg.op(config_schema={
            'a': dg.String,
            'b': dg.String,
        })(self.dummy_function)

        with EphemeralNamedDirectory('steve', self.config_package_dir) as temp_dir:
            with open(os.path.join(temp_dir, 'global.yaml'), 'w') as config_yaml_io:
                yaml.dump({'a': 'sneve'}, config_yaml_io)

            preconfigured = self.configurator(op_def, 'mode', additional_schema={'b': dg.String})
            # assert that it accepts no additional config
            fields = preconfigured.get_config_field().config_type.fields
            self.assertEqual(set(fields.keys()), {'b'})
