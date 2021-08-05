"""
TDR snapshot operations
"""
import logging
from enum import Enum

from data_repo_client import RepositoryApi, SnapshotRequestModel, SnapshotRequestContentsModel

from dagster_utils.contrib.data_repo.typing import JobId, ProfileId, DatasetName


class SnapshotMode(Enum):
    BY_ASSET = "byAsset"
    BY_FULL_VIEW = "byFullView"
    BY_ROW_ID = "byRowId"
    BY_QUERY = "byQuery"


def submit_snapshot_request(
        snapshot_name: str,
        profile_id: ProfileId,
        dataset_name: DatasetName,
        mode: SnapshotMode,
        reader_list: list[str],
        data_repo_client: RepositoryApi) -> JobId:
    snapshot_request = SnapshotRequestModel(
        name=snapshot_name,
        profile_id=profile_id,
        description=f"Create snapshot {snapshot_name}",
        contents=[SnapshotRequestContentsModel(dataset_name=dataset_name, mode=mode.value)],
        readers=reader_list
    )

    logging.info(snapshot_request)

    response = data_repo_client.create_snapshot(
        snapshot=snapshot_request
    )

    logging.info(f"Snapshot creation job id: {response.id}")
    return JobId(response.id)
