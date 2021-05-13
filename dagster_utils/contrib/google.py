from typing import Optional

import google.auth
from google.auth.transport.requests import AuthorizedSession, Request
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
