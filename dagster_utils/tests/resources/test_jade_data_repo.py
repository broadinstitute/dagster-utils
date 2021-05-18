import unittest

from dagster_utils.resources.jade_data_repo import build_client

class DataRepoClientTestCase(unittest.TestCase):

    def test_client_auths_successfully(self):
        client = build_client(host='https://jade.datarepo-dev.broadinstitute.org/')
        result = client.enumerate_datasets()