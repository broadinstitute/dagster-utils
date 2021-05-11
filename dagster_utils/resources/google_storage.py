from typing import Iterator
from dataclasses import dataclass

from dagster import resource
from dagster.core.execution.context.init import InitResourceContext

import google.auth
from google.cloud import storage


@resource
def google_storage_client(_: InitResourceContext) -> storage.Client:
    credentials, project = google.auth.default()

    return storage.Client(project=project, credentials=credentials)


@dataclass
class MockBlob:
    name: str
    def delete(self) -> None:
        pass


class MockStorageClient:
    def list_blobs(self, bucket_name: str, prefix: str) -> Iterator[MockBlob]:
        for i in range(0, 10):
            yield MockBlob(f"fake_blob_{i}")


@resource
def mock_storage_client(_: InitResourceContext) -> MockStorageClient:
    return MockStorageClient()
