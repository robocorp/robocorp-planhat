"""Planhat API library for the Robocorp Python Automation Framework

This library provides an interface to the [Planhat API](https://docs.planhat.com/). 
Most of the methods available in the `Planhat` are generic and can
be used to make requests for all the various object endpoints (most objects
have similar calls). You select the endpoint by providing a subclass of
the `types.PlanhatObject` class as the `object_type` parameter.

When creating or modifying (updating/deleting) existing objects, you can
initialize a new `PlanhatObject` with a dictionary of values. The dictionary
keys must match the field names in the Planhat API documentation for the
update or creation to be successful. Delete only requiers the correct ID.
"""
import os
from robocorp import log

if os.getenv("LOG_SECRETS", "false").lower() == "false":
    log.add_sensitive_variable_name("credentials")
    log.add_sensitive_variable_name("headers")
    log.add_sensitive_variable_name("api_key")
    log.add_sensitive_variable_name("tenant_uuid")

__version__ = "0.4.7"

from .client import PlanhatClient as Planhat
from . import types
from .errors import (
    PlanhatHTTPError,
    PlanhatAuthConfigurationError,
    PlanhatAuthFailedError,
    PlanhatRateLimitError,
    PlanhatNotFoundError,
    PlanhatServerError,
    PlanhatBadRequestError,
)

__all__ = [
    "Planhat",
    "types",
    "PlanhatHTTPError",
    "PlanhatAuthConfigurationError",
    "PlanhatAuthFailedError",
    "PlanhatRateLimitError",
    "PlanhatNotFoundError",
    "PlanhatServerError",
    "PlanhatBadRequestError",
]
