from dataclasses import dataclass

from dagster import resource, StringSource, Field
from dagster.core.execution.context.init import InitResourceContext

from data_repo_client import ApiClient, Configuration, RepositoryApi

from dagster_utils.contrib.google import default_google_access_token


@resource({
    "api_url": Field(StringSource)
})
def jade_data_repo_client(init_context: InitResourceContext) -> RepositoryApi:
    config = Configuration(host=init_context.resource_config["api_url"])
    config.access_token = default_google_access_token()
    client = ApiClient(configuration=config)
    client.client_side_validation = False

    return RepositoryApi(api_client=client)


class NoopDataRepoClient:
    @dataclass
    class NoopResult:
        total: int

    @dataclass
    class FakeJobResponse:
        completed: bool
        id: str
        job_status: str

    def enumerate_datasets(self) -> NoopResult:
        return NoopDataRepoClient.NoopResult(5)

    def retrieve_job(self, job_id: str) -> FakeJobResponse:
        return NoopDataRepoClient.FakeJobResponse(True, "abcdef", "succeeded")

    def bulk_file_load(self, dataset_id: str, bulk_file_load: dict[str, str]) -> FakeJobResponse:
        return NoopDataRepoClient.FakeJobResponse(True, "abcdef", "succeeded")

    def retrieve_job_result(self, job_id: str) -> dict[str, int]:
        return {
            "failedFiles": 0
        }

@resource
def noop_data_repo_client(init_context: InitResourceContext) -> NoopDataRepoClient:
    return NoopDataRepoClient()
