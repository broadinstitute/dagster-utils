import os
from tempfile import TemporaryDirectory
import unittest
import warnings
import yaml


import dagster_utils.config
from dagster_utils.config.preconfiguration_loader import PreconfigurationLoader


class PreconfigurationLoaderTestCase(unittest.TestCase):
    def setUp(self):
        self.config_package_dir = os.path.dirname(dagster_utils.config.__file__)

    def test_validated_config_raises_if_missing_keys(self):
        loader = PreconfigurationLoader(
            name="foo",
            config_file_directory="bar/baz",
            optional_keys=set(),
            required_keys={'a', 'b', 'c'}
        )

        with self.assertRaisesRegex(ValueError, 'Missing expected preconfigured field'):
            loader.validated_config({'a': 'value'})

    def test_validated_config_does_not_raise_if_missing_optional_keys(self):
        loader = PreconfigurationLoader(
            name="foo",
            config_file_directory="bar/baz",
            optional_keys={'b', 'c'},
            required_keys={'a'},
        )
        self.assertEqual(
            loader.validated_config({'a': 'value', 'b': 'thing'}),
            {'a': 'value', 'b': 'thing'}
        )

    def test_validated_config_warns_and_cuts_if_extra_keys(self):
        loader = PreconfigurationLoader(
            name="foo",
            config_file_directory="bar/baz",
            optional_keys=set(),
            required_keys={'a'},
        )

        with warnings.catch_warnings(record=True) as caught_warnings:
            # ensure no warnings are swallowed
            warnings.simplefilter("always")

            self.assertEqual(
                loader.validated_config({'a': 'value', 'b': 'thing'}),
                {'a': 'value'}
            )

            self.assertEqual(len(caught_warnings), 1)
            self.assertEqual(caught_warnings[0].category, UserWarning)
            self.assertIn("Found unexpected fields", str(caught_warnings[0].message))

    def test_validated_config_returns_unaltered_if_all_keys_present(self):
        loader = PreconfigurationLoader(
            name="foo",
            config_file_directory="bar/baz",
            optional_keys=set(),
            required_keys={'a', 'b'},
        )
        self.assertEqual(
            loader.validated_config({'a': 'value', 'b': 'thing'}),
            {'a': 'value', 'b': 'thing'}
        )

    def test_load_files_raises_if_no_files_present(self):
        with TemporaryDirectory(dir=self.config_package_dir) as temp_dir:
            loader = PreconfigurationLoader(
                name="foo",
                config_file_directory=temp_dir,
                optional_keys=set(),
                required_keys=set()
            )
            with self.assertRaises(FileNotFoundError):
                loader.load_files(['nonexistent.yaml', 'nope.yaml'])

    def test_load_files_returns_only_present_files(self):
        with TemporaryDirectory(dir=self.config_package_dir) as temp_dir:
            loader = PreconfigurationLoader(
                name="foo",
                config_file_directory=temp_dir,
                optional_keys=set(),
                required_keys={'x'},
            )
            with open(os.path.join(temp_dir, 'thing.yaml'), 'w') as existing_yaml_io:
                yaml.dump({'x': 'y'}, existing_yaml_io)
            files = loader.load_files(['not_there.yaml', 'thing.yaml'])
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0], {'x': 'y'})

    def test_load_for_mode_gives_precedent_to_mode_specific(self):
        with TemporaryDirectory(dir=self.config_package_dir) as temp_dir:
            loader = PreconfigurationLoader(
                name="foo",
                config_file_directory=temp_dir,
                optional_keys=set(),
                required_keys={'x', 'y'}
            )
            with open(os.path.join(temp_dir, 'global.yaml'), 'w') as existing_yaml_io:
                yaml.dump({'x': 'y', 'y': 'z'}, existing_yaml_io)

            with open(os.path.join(temp_dir, 'some_mode.yaml'), 'w') as existing_yaml_io:
                yaml.dump({'x': 'abc'}, existing_yaml_io)

            loaded_info = loader.load_for_mode('some_mode')
            self.assertEqual(loaded_info, {'x': 'abc', 'y': 'z'})

    def test_load_for_mode_works_with_global_only(self):
        with TemporaryDirectory(dir=self.config_package_dir) as temp_dir:
            loader = PreconfigurationLoader(
                name="foo",
                config_file_directory=temp_dir,
                optional_keys=set(),
                required_keys={'x', 'y'}
            )
            with open(os.path.join(temp_dir, 'global.yaml'), 'w') as existing_yaml_io:
                yaml.dump({'x': 'y', 'y': 'z'}, existing_yaml_io)

            loaded_info = loader.load_for_mode('some_mode')
            self.assertEqual(loaded_info, {'x': 'y', 'y': 'z'})
