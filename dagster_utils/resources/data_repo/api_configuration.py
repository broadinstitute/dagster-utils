
import data_repo_client
from google.auth.transport.requests import Request


class RefreshingAccessTokenConfig(data_repo_client.Configuration):
    """
    Helper class that hooks access to the access_token property so we can
    intercept and potentially refresh if expired
    """

    def __init__(self, host, google_credentials):
        super().__init__(host)
        self._google_credentials = google_credentials

    @property
    def access_token(self):
        # if creds are expired, attempt to refresh
        if not self._google_credentials.valid:
            self._google_credentials.refresh(Request())
        self._access_token = self._google_credentials.token
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value
