from dataclasses import dataclass

from dagster import resource, StringSource, Field
from dagster.core.execution.context.init import InitResourceContext

from data_repo_client import ApiClient, Configuration, RepositoryApi

from dagster_utils.contrib.google import default_google_access_token, get_credentials


@resource({
    "api_url": Field(StringSource)
})
def jade_data_repo_client(init_context: InitResourceContext) -> RepositoryApi:
    config = Configuration(
        host=init_context.resource_config["api_url"],
        api_key={'Authorization': None},  # will be overwritten when we generate a request, see below
        api_key_prefix={'Authorization': 'Bearer'},
    )

    # not an attribute of the Configuration class - we use this in the below method.
    config._gcloud_credentials = get_credentials()

    # The data repo client calls this function every time it tries to build the
    # authorization headers for a new request, so we'll have a new token generated for each request.
    def refresh_configured_api_key(conf: Configuration) -> None:
        conf.api_key['Authorization'] = default_google_access_token(conf._datarepo_gcloud_credentials)

    config.refresh_api_key_hook = refresh_configured_api_key

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
