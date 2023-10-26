"""Provides Planhat session functionality."""
import requests
from requests.auth import AuthBase
from typing import Any

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from robocorp import log

from .types import PlanhatObject
from .errors import (
    PlanhatAuthFailedError,
    PlanhatAuthConfigurationError,
    PlanhatHTTPError,
    PlanhatNotFoundError,
    PlanhatRateLimitError,
    PlanhatServerError,
)

STATUS_CODES_TO_RETRY = [429, 500, 504]
BASE_PH_URL = "https://api.planhat.com"
BASE_PH_ANALYTICS_URL = "https://analytics.planhat.com"

PlanhatDataType = PlanhatObject | list[PlanhatObject]
JsonDictType = dict[str, Any]
JsonListType = list[JsonDictType]
JsonType = JsonDictType | JsonListType


class PlanhatAuth(AuthBase):
    """Attaches HTTP Authorization to the given Request object."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """Attaches HTTP Authorization to the given Request object."""
        request.headers["Authorization"] = f"Bearer {self.api_key}"
        return request


class PlanhatSession(requests.Session):
    """A Planhat session."""

    def __init__(
        self,
        api_key: str | None = None,
        vault_secret_name: str | None = None,
        tenant_uuid: str | None = None,
    ):
        """Initializes the Planhat session. If you want to use a non-default
        secret or provide the API key directly, you can do so by providing
        the `api_key` and `vault_secret_name` parameters, otherwise
        the default vault secret `planhat_api` is used.
        """
        self._api_key = api_key
        self._tenant_uuid = tenant_uuid
        self._vault_secret_name = vault_secret_name
        super().__init__()
        self._prepare()
        self._api_host = BASE_PH_URL
        self._analytics_host = BASE_PH_ANALYTICS_URL

    def _prepare(self) -> None:
        """Prepares the session. Raises an exception if default
        authentication is not configured.
        """
        self.authenticate()
        self.headers.update(self._create_headers())

    def _create_headers(self) -> dict:
        """Creates the appropriate headers for a Planhat request."""
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def authenticate(
        self,
        api_key: str | None = None,
        vault_secret_name: str | None = None,
        tenant_uuid: str | None = None,
    ) -> None:
        """Configures session authentication.

        :param api_key: The Planhat API key.
        :param vault_secret_name: The name of the vault secret containing the Planhat API key.
            If you provide an API key, this parameter is ignored. The provided vault
            secret must have a key named `api_key`. It may also have a key names
            `tenant_uuid` which is used for analytics calls.
        :param tenant_uuid: The Planhat tenant UUID needed to post analytics If not
            provided, the vault object is checked for a key named `tenant_uuid`. If
            the key is not found, the tenant UUID is not set and analytics calls will
            fail.
        """
        if vault_secret_name is not None:
            self._vault_secret_name = vault_secret_name
        if api_key is not None:
            self._api_key = api_key
        if tenant_uuid is not None:
            self._tenant_uuid = tenant_uuid
        if (
            self._api_key is None
            and self._tenant_uuid is None
            and self._vault_secret_name is not None
        ):
            self._load_credentials()
        if self._api_key is not None:
            self.auth = PlanhatAuth(self._api_key)
        else:
            self.auth = None

    def _load_credentials(self) -> None:
        """Loads credentials from saved vault secret name."""
        # Import these only when needed to avoid missing Environment variables
        # when importing the library.
        if self._vault_secret_name is None:
            raise PlanhatAuthConfigurationError(
                "No Planhat vault secret name provided. Please authenticate with a "
                "Planhat API key or provide a vault secret name."
            )
        from robocorp import vault
        from robocorp.vault import _errors as vault_errors

        try:
            credentials = vault.get_secret(self._vault_secret_name)
        except vault_errors.RobocorpVaultError:
            log.warn(
                f"Could not find vault secret {self._vault_secret_name}. "
                f"Please provide a vault secret with a key named `api_key`."
            )
            credentials = {}
        self._api_key = credentials.get("api_key", None)
        self._tenant_uuid = credentials.get("tenant_uuid", None)

    def _require_api_key(self) -> None:
        """Raises an exception if the API key is not set."""
        if self._api_key is None:
            raise PlanhatAuthConfigurationError(
                f"No Planhat API key provided. Please authenticate with a Planhat API key "
                f"or provide a vault secret with a Planhat API key."
            )

    def _require_tenant_uuid(self) -> None:
        """Raises an exception if the tenant UUID is not set."""
        if self._tenant_uuid is None:
            raise PlanhatAuthConfigurationError(
                f"No Planhat tenant UUID provided. Please authenticate with a tenant "
                f"UUID or provide a vault secret with a tenant UUID."
            )

    @retry(
        retry=retry_if_exception_type(PlanhatRateLimitError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(),
    )
    def _request(
        self,
        method: str,
        url: str,
        params: dict | None = None,
        data: Any | None = None,
        json: JsonType | None = None,
        headers: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Makes a request to the Planhat API.

        :param method: The HTTP method to use.
        :param url: The URL to make the request to. If the URL does not start with
            `http`, the URL is appended to the Planhat API host.
        :param params: The query parameters to use.
        :param data: The data to send in the request body.
        :param json: The JSON data to send in the request body.
        :param headers: The headers to use.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat API.
        """
        self._require_api_key()
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self._api_host}{url}"

        response = super().request(
            method,
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs,
        )
        self._handle_response(response)
        return response

    def _handle_response(self, response: requests.Response) -> None:
        """Handles the response from the Planhat API.

        :param response: The response from the Planhat API.
        """
        if response.status_code >= 200 and response.status_code < 300:
            return
        else:
            server_message = f"Server message: {response.text}"
            if response.status_code in STATUS_CODES_TO_RETRY:
                raise PlanhatRateLimitError(
                    message=f"Planhat rate limit reached. {server_message}",
                    code="planhat_rate_limit",
                    response=response,
                )
            if response.status_code == 403:
                raise PlanhatAuthFailedError(
                    message=f"Planhat permission or authentication error. {server_message}",
                    code="planhat_auth_failed",
                    response=response,
                )
            if response.status_code == 404:
                raise PlanhatNotFoundError(
                    message=f"Planhat resource not found. {server_message}",
                    code="planhat_not_found",
                    response=response,
                )
            if response.status_code >= 500:
                raise PlanhatServerError(
                    message=f"Planhat server error. {server_message}",
                    code="planhat_server_error",
                    response=response,
                )
            raise PlanhatHTTPError(
                message=f"Planhat unspecified HTTP error. {server_message}",
                code="planhat_http_error",
                response=response,
            )

    def get(
        self,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Makes a GET request to the Planhat API.

        :param url: The URL to make the request to. If the URL does not start with
            `http`, the URL is appended to the Planhat API host.
        :param params: The query parameters to use.
        :param headers: The headers to use.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat API.
        """
        return self._request("GET", url, params=params, headers=headers, **kwargs)

    def post(
        self,
        url: str,
        data: Any | None = None,
        json: PlanhatDataType | None = None,
        headers: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Makes a POST request to the Planhat API.

        :param url: The URL to make the request to. If the URL does not start with
            `http`, the URL is appended to the Planhat API host.
        :param data: The data to send in the request body.
        :param json: The JSON data to send in the request body.
        :param headers: The headers to use.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat API.
        """
        return self._request(
            "POST", url, data=data, json=json, headers=headers, **kwargs
        )

    def put(
        self,
        url: str,
        data: Any | None = None,
        json: PlanhatDataType | None = None,
        headers: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Makes a PUT request to the Planhat API.

        :param url: The URL to make the request to. If the URL does not start with
            `http`, the URL is appended to the Planhat API host.
        :param data: The data to send in the request body.
        :param json: The JSON data to send in the request body.
        :param headers: The headers to use.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat API.
        """
        return self._request(
            "PUT", url, data=data, json=json, headers=headers, **kwargs
        )

    def patch(
        self,
        url: str,
        data: Any | None = None,
        json: PlanhatDataType | None = None,
        headers: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Makes a PATCH request to the Planhat API.

        :param url: The URL to make the request to. If the URL does not start with
            `http`, the URL is appended to the Planhat API host.
        :param data: The data to send in the request body.
        :param json: The JSON data to send in the request body.
        :param headers: The headers to use.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat API.
        """
        return self._request(
            "PATCH", url, data=data, json=json, headers=headers, **kwargs
        )

    def delete(
        self,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Makes a DELETE request to the Planhat API.

        :param url: The URL to make the request to. If the URL does not start with
            `http`, the URL is appended to the Planhat API host.
        :param params: The query parameters to use.
        :param headers: The headers to use.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat API.
        """
        return self._request("DELETE", url, params=params, headers=headers, **kwargs)

    def _request_analytics(
        self,
        url: str,
        data: Any | None = None,
        json: JsonType | None = None,
        headers: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Makes a request to the Planhat Analytics API.

        :param url: The URL to make the request to. If the URL does not start with
            `http`, the URL is appended to the Planhat Analytics host.
        :param data: The data to send in the request body.
        :param json: The JSON data to send in the request body.
        :param headers: The headers to use.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat Analytics API.
        """
        self._require_tenant_uuid()
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if json is None:
            json = {}
        if not url.startswith("http"):
            url = f"{self._analytics_host}/{url}/{self._tenant_uuid}"

        response = super().request(
            "POST", url, data=data, json=json, headers=headers, **kwargs
        )
        self._handle_response(response)
        return response

    def create_analytics(
        self,
        activity: JsonDictType,
        **kwargs: Any,
    ) -> requests.Response:
        """Creates an activity in Planhat.

        :param activity: The activity to create.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat API.
        """
        return self._request_analytics("analytics", json=activity, **kwargs)

    def create_bulk_activities(
        self,
        activities: JsonListType,
        **kwargs: Any,
    ) -> requests.Response:
        """Creates a bulk of activities in Planhat.

        :param activities: The activities to create.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: The response from the Planhat API.
        """
        return self._request_analytics("analytics/bulk", json=activities, **kwargs)
