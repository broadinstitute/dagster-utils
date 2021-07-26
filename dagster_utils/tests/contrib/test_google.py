import pytest

from dagster_utils.contrib.google import parse_gs_path, GsBucketWithPrefix


def test_parse_gs_path():
    raw_path = "gs://example/bucket/path"

    result = parse_gs_path(raw_path)

    assert result.bucket == "example"
    assert result.prefix == "bucket/path"


def test_parse_gs_path_rejects_non_gs_paths():
    raw_path = "bucket/path"

    with pytest.raises(ValueError):
        parse_gs_path(raw_path)


def test_maps_object_back_to_path():
    object = GsBucketWithPrefix("bucket", "path/prefix")

    result = object.to_gs_path()

    assert result == "gs://bucket/path/prefix"
