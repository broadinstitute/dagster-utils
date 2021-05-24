import time
from typing import Any
import logging

from data_repo_client import RepositoryApi

from dagster_utils.contrib.data_repo.typing import JobId


class JobPollException(Exception):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args)
        self.message = kwargs.get('message')


class JobFailureException(JobPollException):
    pass


class JobTimeoutException(JobPollException):
    pass


def poll_job(
        job_id: JobId,
        max_wait_time_seconds: int,
        poll_interval_seconds: int,
        data_repo_client: RepositoryApi
) -> JobId:
    """
    Polls on the given TDR job_id for max_wait_time_seconds, every poll_interval_seconds, until the job is reported
    completed or we time out.
    """
    time_waited = 0

    while time_waited < max_wait_time_seconds:
        logging.info(f"Polling on data repo job_id = {job_id}...")
        job_info = data_repo_client.retrieve_job(job_id)

        if job_info.completed:
            logging.info(f"Data repo job_id = {job_id} completed")
            if job_info.job_status == "failed":
                raise JobFailureException(
                    message="Job did not complete successfully."
                )
            return job_id

        logging.info(f"Data repo job_id = {job_id} not complete, scheduling retry...")
        time.sleep(poll_interval_seconds)
        time_waited += poll_interval_seconds

    raise JobTimeoutException(
        message=f"Exceeded max wait time of {max_wait_time_seconds} polling for status of job {job_id}."
    )
