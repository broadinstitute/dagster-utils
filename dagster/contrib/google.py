from typing import Optional
from dataclasses import dataclass
from urllib.parse import urlparse

import google.auth
from google.auth.transport.requests import AuthorizedSession, Request
from google.cloud.storage.client import Client
from google.oauth2.credentials import Credentials

DEFAULT_SCOPES = ['openid', 'email', 'profile', 'https://www.googleapis.com/auth/cloud-platform']


def google_default() -> tuple[Credentials, str]:
    return google.auth.default(scopes=DEFAULT_SCOPES)  # type: ignore # (unannotated library)


def get_credentials() -> Credentials:
    creds, _ = google_default()
    return creds


def default_google_access_token(credentials: Optional[Credentials] = None) -> str:
    """
    Get token for Google-based auth use.
    Assumes application default credentials work for specified environment.
    Note that this token will only be valid for 60 minutes. For uses that may need to
    make requests for longer than this, use an AuthorizedSession (which auto-refreshes the token).
    """
    credentials = credentials or get_credentials()
    credentials.refresh(Request())

    return credentials.token  # type: ignore # (unannotated library)


def authorized_session() -> AuthorizedSession:
    return AuthorizedSession(get_credentials())


def gs_path_from_bucket_prefix(bucket: str, prefix: str) -> str:
    return f"gs://{bucket}/{prefix}"


def path_has_any_data(bucket: str, prefix: str, gcs: Client) -> bool:
    """Checks the given path for any blobs of non-zero size"""
    blobs = [blob for blob in
             gcs.list_blobs(bucket, prefix=prefix)]
    return any([blob.size > 0 for blob in blobs])


@dataclass
class GsBucketWithPrefix:
    bucket: str
    prefix: str

    def to_gs_path(self) -> str:
        return f"gs://{self.bucket}/{self.prefix}"


def parse_gs_path(raw_gs_path: str) -> GsBucketWithPrefix:
    if not raw_gs_path.startswith("gs://"):
        raise ValueError("GS path must being with gs:// scheme")
    url_result = urlparse(raw_gs_path)
    return GsBucketWithPrefix(url_result.netloc, url_result.path[1:])
