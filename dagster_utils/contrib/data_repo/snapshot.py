import logging

from data_repo_client import RepositoryApi, SnapshotRequestModel, SnapshotRequestContentsModel

from dagster_utils.contrib.data_repo.typing import JobId


def submit_snapshot_request(
        snapshot_name: str,
        profile_id: str,
        dataset_name,
        mode: str,
        reader_list: list[str],
        data_repo_client: RepositoryApi) -> JobId:
    snapshot_request = SnapshotRequestModel(
        name=snapshot_name,
        profile_id=profile_id,
        description=f"Create snapshot {snapshot_name}",
        contents=[SnapshotRequestContentsModel(dataset_name=dataset_name, mode=mode)],
        readers=reader_list
    )

    logging.info(snapshot_request)

    response = data_repo_client.create_snapshot(
        snapshot=snapshot_request
    )

    logging.info(f"Snapshot creation job id: {response.id}")
    return JobId(response.id)