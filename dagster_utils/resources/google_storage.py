from typing import Iterator
from dataclasses import dataclass

from dagster import resource
from dagster.core.execution.context.init import InitResourceContext

from google.cloud import storage

from dagster_utils.contrib.google import authorized_session, google_default


@resource
def google_storage_client(_: InitResourceContext) -> storage.Client:
    _, project = google_default()

    return storage.Client(project=project, _http=authorized_session())


@dataclass
class MockBlob:
    name: str
    size: int

    def delete(self) -> None:
        pass


class MockStorageClient:
    def list_blobs(self, bucket_name: str, prefix: str) -> Iterator[MockBlob]:
        for i in range(0, 10):
            yield MockBlob(f"fake_blob_{i}", 1)


@resource
def mock_storage_client(_: InitResourceContext) -> MockStorageClient:
    return MockStorageClient()
