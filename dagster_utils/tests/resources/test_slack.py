import os
import unittest
from unittest import mock

from dagster_utils.resources.slack import live_slack_client, LiveSlackClient
from dagster_utils.testing.resources import initialize_resource


class LiveSlackResourceTestCase(unittest.TestCase):
    @mock.patch.dict(os.environ, {
        **os.environ,
        'SLACK_TOKEN': 'jeepers',
    })
    def test_resource_can_be_initialized(self):
        with initialize_resource(live_slack_client, config={'channel': '#something'}) as client_instance:
            self.assertIsInstance(client_instance, LiveSlackClient)
