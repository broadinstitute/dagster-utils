from urllib.parse import urljoin
from dataclasses import dataclass

from dagster import Field, resource, StringSource
from dagster.core.execution.context.init import InitResourceContext
from google.auth.transport.requests import AuthorizedSession

from dagster_utils.contrib.google import authorized_session


@dataclass
class Sam:
    base_url: str

    def set_public_flag(self, snapshot_id: str, status: bool) -> None:
        # we are explicitly set content-type in this PUT as the requests lib only sets it when
        # using the json= kwarg, and SAM will 415 otherwise
        response = self._session().put(
            self._api_url(f'api/resources/v1/datasnapshot/{snapshot_id}/policies/reader/public'),
            headers={"Content-type": "application/json"},
            data=f"{str(status).lower()}",  # telling the endpoint to set the flag to true/false
        )

        # raise an exception for a bad response
        response.raise_for_status()

    # private methods

    def _api_url(self, url_part: str) -> str:
        return urljoin(self.base_url, url_part)

    def _session(self) -> AuthorizedSession:
        return authorized_session()


@resource({
    "api_url": Field(StringSource)
})
def sam_client(init_context: InitResourceContext) -> Sam:
    return Sam(base_url=init_context.resource_config['api_url'])


class NoopSamClient:
    def make_snapshot_public(self, snapshot_id: str) -> None:
        pass


@resource
def noop_sam_client(init_context: InitResourceContext) -> NoopSamClient:
    return NoopSamClient()
