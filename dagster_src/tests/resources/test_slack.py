import unittest

from dagster_src.resources.slack import live_slack_client, LiveSlackClient
from dagster_src.testing.resources import initialize_resource
from dagster_src.dagster_typing import DagsterConfigDict


class LiveSlackResourceTestCase(unittest.TestCase):
    def test_resource_can_be_initialized(self):
        test_config: DagsterConfigDict = {'channel': '#something', 'token': 'aeiou'}
        with initialize_resource(live_slack_client, config=test_config) as client_instance:
            self.assertIsInstance(client_instance, LiveSlackClient)
