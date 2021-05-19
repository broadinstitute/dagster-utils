import unittest
from unittest.mock import Mock

from dagster_utils.resources.data_repo.api_configuration import RefreshingAccessTokenConfig
from dagster_utils.contrib.google import Credentials


class RefreshingConfigurationTestCase(unittest.TestCase):
    def test_refreshing_configuration_delegates_access_token(self):
        creds = Mock(spec=Credentials)
        creds.token = "faketoken!"
        creds.valid = True

        config = RefreshingAccessTokenConfig("http://example.com", creds)

        self.assertEqual(config.access_token, "faketoken!")
        # valid creds should not require refresh
        creds.refresh.assert_not_called

    def test_refreshing_configuration_refreshes_on_invalid_token(self):
        creds = Mock(spec=Credentials)
        creds.token = "faketoken!"
        creds.valid = False

        config = RefreshingAccessTokenConfig("http://example.com", creds)

        self.assertEqual(config.access_token, "faketoken!")
        # invalid creds should refresh
        creds.refresh.assert_called_once
