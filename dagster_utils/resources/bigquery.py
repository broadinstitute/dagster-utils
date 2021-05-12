from google.cloud.bigquery import Dataset, Client
from dagster import resource, InitResourceContext

from dagster_utils.contrib.google import authorized_session


@resource
def bigquery_client(init_context: InitResourceContext) -> Client:
    return Client(_http=authorized_session())


class NoopBigQueryClient:
    def create_dataset(self, dataset: Dataset) -> None:
        pass


@resource
def noop_bigquery_client(init_context: InitResourceContext) -> Client:
    return NoopBigQueryClient()
