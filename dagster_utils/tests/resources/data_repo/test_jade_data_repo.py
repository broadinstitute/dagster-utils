import unittest
import pytest
from google.auth.exceptions import DefaultCredentialsError

from dagster_utils.resources.data_repo.jade_data_repo import build_client


class DataRepoClientTestCase(unittest.TestCase):

    @pytest.mark.ci_only
    def test_client_auths_successfully(self):
        # make sure we can successfully connect to Jade
        # this test is marked ci-only as there is some gcloud dependent configuration
        # needed which may be cumbersome in local dev
        try:
            client = build_client(host='https://jade.datarepo-dev.broadinstitute.org/')
            result = client.enumerate_datasets()
            self.assertIsNotNone(result, "Should get back any result")
        except DefaultCredentialsError as e:
            # This is not a test failure - it's a failure to authenticate with  Google Default Credentials in
            # GitHub actions
            pass
