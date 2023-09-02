"""
Common TDR ingestion functions.
"""
import logging

from data_repo_client.api.repository_api import RepositoryApi
from google.cloud.bigquery.client import Client

from dagster_utils.contrib.data_repo.typing import JobId, DatasetId, DatasetName


def ingest_tabular_json_data(
        path: str,
        table: str,
        target_dataset_id: DatasetId,
        data_repo_client: RepositoryApi,
) -> JobId:
    """
    Given a GS path with tabular JSON data, submits the data for ingestion to TDR
    :param path: A GS path; makes no assertions about the state of permissions on the path
    :param table: Target table in TDR for the data
    :param target_dataset_id: Target dataset ID of the data
    :param data_repo_client: Datarepo client appropriate for the target dataset's environment (dev, prod, etc.)
    :return: Job ID for the TDR ingestion job
    """
    if not path.startswith("gs://"):
        raise ValueError("Path must be a gs:// url")

    ingest_payload = {
        "format": "json",
        "ignore_unknown_values": "false",
        "max_bad_records": 0,
        "path": path,
        "table": table,
    }

    job_response = data_repo_client.ingest_dataset(
        id=target_dataset_id, ingest=ingest_payload
    )
    job_id = JobId(job_response.id)
    logging.info(f"Ingest job for table {table} submitted, job_id = {job_id}")

    return job_id


def find_outdated_rows_csv(
        target_dataset_project_id: str,
        target_dataset_name: DatasetName,
        table_name: str,
        primary_keys: set[str],
        version_key: str,
        outdated_ids_path: str,
        bigquery_client: Client
) -> None:
    """
    Determines rows that are outdated in a given table, assuming a monotonically increasing versioning key.
    This function assumes rows are outdated when there is a duplicate row with the same primary key and a strictly
    _higher_ value for it's version field

    :param target_dataset_project_id: Target BQ project ID
    :param target_dataset_name: Target TDR dataset name
    :param table_name: Table name to inspect for outdated rows
    :param primary_keys: Set of keys that uniquely identify a row
    :param version_key: Field on the table that should always be _higher_ for semantically newer data
    :param outdated_ids_path: Path which will receive the CSV of outdated rows
    :param bigquery_client:  BQ client
    """
    if not primary_keys:
        raise ValueError("primary_keys should be non-empty")

    if not outdated_ids_path.startswith("gs://"):
        raise ValueError("outdated_ids_path should be a gs URL")

    fully_qualified_table_name = f"{target_dataset_project_id}.datarepo_{target_dataset_name}.{table_name}"
    joined_primary_keys = ", ".join(primary_keys)
    join_points = [
        f"j.{key} = s.{key}" for key in primary_keys
    ]
    join_clause = " AND ".join(join_points)

    query = f"""
        EXPORT DATA OPTIONS(
            uri='{outdated_ids_path}',
            format='CSV',
            overwrite=true
        ) AS
        WITH latest_versions AS (
            SELECT {joined_primary_keys}, max({version_key}) as latest_version FROM `{fully_qualified_table_name}`
            GROUP BY {joined_primary_keys}
        )
        SELECT s.datarepo_row_id FROM `{fully_qualified_table_name}` s
        INNER JOIN latest_versions j ON {join_clause} WHERE s.{version_key} < j.latest_version
    """

    bigquery_client.query(query).result()


def submit_soft_deletes_csv(path: str, target_dataset_id: DatasetId, data_repo_client: RepositoryApi) -> JobId:
    """
    Submits a path containing CSV(s) of TDR row IDs for soft deletion
    :param path: GS path containing the CSV(s)
    :param target_dataset_id: TDR target dataset
    :param data_repo_client: Datarepo client appropriate for the target dataset's environment (dev, prod, etc.)
    :return: Job ID for the TDR soft deletion job
    """
    if not path.startswith("gs://"):
        raise ValueError("path should be a gs url")

    payload = {
        "deleteType": "soft",
        "specType": "gcsFile",
        "tables": [
            {
                "gcsFileSpec": {"fileType": "csv", "path": path},
                "tableName": "weather_data",
            }
        ],
    }

    job_response = data_repo_client.apply_dataset_data_deletion(
        id=target_dataset_id, data_deletion_request=payload
    )

    job_id = JobId(job_response.id)
    return job_id
