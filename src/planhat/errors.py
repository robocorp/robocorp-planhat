from ast import arg
from urllib import request
from requests.exceptions import HTTPError


class PlanhatError(Exception):
    """Base class for all Planhat API errors."""


class PlanhatHTTPError(PlanhatError, HTTPError):
    """Base class for all Planhat API Session errors."""

    def __init__(
        self, message: str | None = None, code: str | None = None, *args, **kwargs
    ):
        response = kwargs.pop("response", None)
        request = kwargs.pop("request", None)
        HTTPError.__init__(self, message, response=response, request=request)
        PlanhatError.__init__(self, message, code)


class PlanhatAuthConfigurationError(PlanhatError):
    "Error when authentication is not configured correctly."


class PlanhatAuthFailedError(PlanhatHTTPError):
    "Error when authentication fails or the API server returns a 403 error."


class PlanhatRateLimitError(PlanhatHTTPError):
    "Error when the API's rate limits are exceeded."


class PlanhatNotFoundError(PlanhatHTTPError):
    "Error when the requested resource is not found."


class PlanhatServerError(PlanhatHTTPError):
    "Error when the API server returns a 5xx error."


class PlanhatBadRequestError(PlanhatHTTPError):
    "Error when the API server returns a 400 error."
