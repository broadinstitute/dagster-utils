from google.cloud.bigquery import Dataset, Client
from dagster import resource, InitResourceContext
from dagster_utils.contrib.google import get_credentials

from unittest.mock import Mock


@resource
def bigquery_client(init_context: InitResourceContext) -> Client:
    return Client(credentials=get_credentials())


@resource
def noop_bigquery_client(init_context: InitResourceContext) -> Client:
    return Mock(spec=Client)
