import unittest
from unittest.mock import MagicMock, patch

from dagster_utils.resources.sam import sam_client, Sam
from dagster_utils.testing.resources import initialize_resource
from dagster_utils.testing.matchers import StringEndingWith
from dagster_utils.typing import DagsterConfigDict


class SamResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.dummy_config: DagsterConfigDict = {'api_url': 'https://example.com'}

    def test_resource_can_be_initialized_without_extra_config(self):
        with initialize_resource(sam_client, config=self.dummy_config) as client_instance:
            self.assertIsInstance(client_instance, Sam)

    def test_make_snapshot_public_hits_expected_url(self):
        with initialize_resource(sam_client, config=self.dummy_config) as client_instance:
            mock_authorized_session = MagicMock()
            with patch('dagster_utils.resources.sam.Sam._session', return_value=mock_authorized_session):
                client_instance.make_snapshot_public('fake-snapshot-id')
                mock_authorized_session.put.assert_called_once_with(
                    StringEndingWith('datasnapshot/fake-snapshot-id/policies/reader/public'),
                    headers={"Content-type": "application/json"},
                    data="true"
                )
