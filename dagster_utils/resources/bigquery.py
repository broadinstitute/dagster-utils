from google.cloud.bigquery import Dataset, Client
from dagster import resource, InitResourceContext

from dagster_utils.contrib.google import authorized_session

from unittest.mock import Mock


@resource
def bigquery_client(init_context: InitResourceContext) -> Client:
    return Client(_http=authorized_session())


@resource
def noop_bigquery_client(init_context: InitResourceContext) -> Client:
    return Mock(spec=Client)
