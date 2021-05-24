import unittest
from unittest.mock import Mock

from data_repo_client import RepositoryApi
from dagster_utils.contrib.data_repo.jobs import poll_job, JobFailureException, JobTimeoutException
from dagster_utils.contrib.data_repo.typing import JobId


class PollJobTestCase(unittest.TestCase):
    def setUp(self):
        self.data_repo_client = Mock(spec=RepositoryApi)

    def test_returns_success_on_job_complete(self):
        result = poll_job(
            JobId("fake_job_id"),
            2,
            1,
            self.data_repo_client
        )

        self.assertEqual(result, "fake_job_id")

    def test_raises_on_poll_timeout(self):
        job_status_result = Mock()
        job_status_result.completed = False
        self.data_repo_client.retrieve_job = Mock(return_value=job_status_result)

        with self.assertRaises(JobTimeoutException):
            result = poll_job(
                JobId("fake_job_id"),
                2,
                1,
                self.data_repo_client
            )

            self.assertEqual(result, "fake_job_id")

    def test_raises_on_job_failure(self):
        job_status_result = Mock()
        job_status_result.completed = True
        job_status_result.job_status = 'failed'
        self.data_repo_client.retrieve_job = Mock(return_value=job_status_result)

        with self.assertRaises(JobFailureException):
            result = poll_job(
                JobId("fake_job_id"),
                2,
                1,
                self.data_repo_client
            )

            self.assertEqual(result, "fake_job_id")
