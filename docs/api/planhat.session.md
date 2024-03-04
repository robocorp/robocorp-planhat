<!-- markdownlint-disable -->

# module `planhat.session`

**Source:** [`session.py:0`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L0)

Provides Planhat session functionality.

## Variables

- **STATUS_CODES_TO_RETRY**
- **BASE_PH_URL**
- **BASE_PH_ANALYTICS_URL**

______________________________________________________________________

## class `PlanhatAuth`

**Source:** [`session.py:37`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L37)

Attaches HTTP Authorization to the given Request object.

### method `__init__`

**Source:** [`session.py:40`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L40)

```python
__init__(api_key: str) → None
```

______________________________________________________________________

## class `PlanhatSession`

**Source:** [`session.py:57`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L57)

A Planhat session.

This class represents a session for interacting with the Planhat API.

Implementation note: This clas mimics the requests.Session class' methods, but does not directly subclass it to avoid typing issues associated with Sessions' method signatures (this class accepts more narrow parameter and header types than the requests.Session class' methods).

### method `__init__`

**Source:** [`session.py:69`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L69)

```python
__init__(
    api_key: str | None = None,
    vault_secret_name: str | None = None,
    tenant_uuid: str | None = None
)
```

Initializes the Planhat session.

If you want to use a non-default secret or provide the API key directly, you can do so by providing the `api_key` and `vault_secret_name` parameters, otherwise the default vault secret `planhat_api` is used.

**Args:**

- <b>`api_key`</b>:  The Planhat API key.
- <b>`vault_secret_name`</b>:  The name of the vault secret containing the Planhat API key.
- <b>`tenant_uuid`</b>:  The Planhat tenant UUID needed to post analytics.

______________________________________________________________________

### method `authenticate`

**Source:** [`session.py:113`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L113)

```python
authenticate(
    api_key: str | None = None,
    vault_secret_name: str | None = None,
    tenant_uuid: str | None = None
) → None
```

Configures session authentication.

**Args:**

- <b>`api_key`</b>:  The Planhat API key.
- <b>`vault_secret_name`</b>:  The name of the vault secret containing the Planhat API key. If an API key is provided, this parameter is ignored. The provided vault secret must have a key named `api_key`. It may also have a key named `tenant_uuid` which is used for analytics calls.
- <b>`tenant_uuid`</b>:  The Planhat tenant UUID needed to post analytics. If not provided, the vault object is checked for a key named `tenant_uuid`. If the key is not found, the tenant UUID is not set and analytics calls will fail.

**Raises:**

- <b>`PlanhatAuthConfigurationError`</b>:  If no Planhat vault secret name is provided.

______________________________________________________________________

### method `create_analytics`

**Source:** [`session.py:510`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L510)

```python
create_analytics(activity: dict[str, Any], **kwargs) → Response
```

Creates an activity in Planhat.

**Args:**

- <b>`activity`</b>:  The activity to create.
- <b>`**kwargs`</b>:  Additional keyword arguments to pass to the request.

**Returns:**
The response from the Planhat API.

**Raises:**

- <b>`PlanhatAuthConfigurationError`</b>:  If the tenant UUID is not set.
- <b>`PlanhatRateLimitError`</b>:  If the API's rate limits are exceeded.
- <b>`PlanhatAuthFailedError`</b>:  If authentication fails or the API server returns a 403 error.
- <b>`PlanhatNotFoundError`</b>:  If the requested resource is not found.
- <b>`PlanhatServerError`</b>:  If the API server returns a 5xx error.
- <b>`PlanhatHTTPError`</b>:  If the API server returns an unspecified HTTP error.

______________________________________________________________________

### method `create_bulk_activities`

**Source:** [`session.py:534`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L534)

```python
create_bulk_activities(
    activities: list[dict[str, Any]],
    **kwargs: Any
) → Response
```

Creates a bulk of activities in Planhat.

**Args:**

- <b>`activities`</b>:  The activities to create.
- <b>`**kwargs`</b>:  Additional keyword arguments to pass to the request.

**Returns:**
The response from the Planhat API.

**Raises:**

- <b>`PlanhatAuthConfigurationError`</b>:  If the tenant UUID is not set.
- <b>`PlanhatRateLimitError`</b>:  If the API's rate limits are exceeded.
- <b>`PlanhatAuthFailedError`</b>:  If authentication fails or the API server returns a 403 error.
- <b>`PlanhatNotFoundError`</b>:  If the requested resource is not found.
- <b>`PlanhatServerError`</b>:  If the API server returns a 5xx error.
- <b>`PlanhatHTTPError`</b>:  If the API server returns an unspecified HTTP error.

______________________________________________________________________

### method `delete`

**Source:** [`session.py:434`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L434)

```python
delete(
    url: str,
    params: Optional[Mapping[str, str | int]] = None,
    headers: Optional[Mapping[str, str]] = None,
    **kwargs
) → Response
```

Makes a DELETE request to the Planhat API.

**Args:**

- <b>`url`</b>:  The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.
- <b>`params`</b>:  The query parameters to use.
- <b>`headers`</b>:  The headers to use.
- <b>`kwargs`</b>:  Additional keyword arguments to pass to the request.

**Returns:**
The response from the Planhat API.

**Raises:**

- <b>`PlanhatAuthConfigurationError`</b>:  If the API key is not set.
- <b>`PlanhatRateLimitError`</b>:  If the API's rate limits are exceeded.
- <b>`PlanhatAuthFailedError`</b>:  If authentication fails or the API server returns a 403 error.
- <b>`PlanhatNotFoundError`</b>:  If the requested resource is not found.
- <b>`PlanhatServerError`</b>:  If the API server returns a 5xx error.
- <b>`PlanhatHTTPError`</b>:  If the API server returns an unspecified HTTP error.

______________________________________________________________________

### method `get`

**Source:** [`session.py:305`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L305)

```python
get(
    url: str,
    params: Optional[Mapping[str, str | int]] = None,
    headers: Optional[Mapping[str, str]] = None,
    **kwargs
) → Response
```

Makes a GET request to the Planhat API.

**Args:**

- <b>`url`</b>:  The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.
- <b>`params`</b>:  The query parameters to use.
- <b>`headers`</b>:  The headers to use.
- <b>`kwargs`</b>:  Additional keyword arguments to pass to the request.

**Returns:**
The response from the Planhat API.

**Raises:**

- <b>`PlanhatAuthConfigurationError`</b>:  If the API key is not set.
- <b>`PlanhatRateLimitError`</b>:  If the API's rate limits are exceeded.
- <b>`PlanhatAuthFailedError`</b>:  If authentication fails or the API server returns a 403 error.
- <b>`PlanhatNotFoundError`</b>:  If the requested resource is not found.
- <b>`PlanhatServerError`</b>:  If the API server returns a 5xx error.
- <b>`PlanhatHTTPError`</b>:  If the API server returns an unspecified HTTP error.

______________________________________________________________________

### method `patch`

**Source:** [`session.py:401`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L401)

```python
patch(
    url: str,
    data: Any | None = None,
    json: PlanhatObject | list[PlanhatObject] | None = None,
    headers: Optional[Mapping[str, str]] = None,
    **kwargs
) → Response
```

Makes a PATCH request to the Planhat API.

**Args:**

- <b>`url`</b>:  The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.
- <b>`params`</b>:  The query parameters to use.
- <b>`headers`</b>:  The headers to use.
- <b>`kwargs`</b>:  Additional keyword arguments to pass to the request.

**Returns:**
The response from the Planhat API.

**Raises:**

- <b>`PlanhatAuthConfigurationError`</b>:  If the API key is not set.
- <b>`PlanhatRateLimitError`</b>:  If the API's rate limits are exceeded.
- <b>`PlanhatAuthFailedError`</b>:  If authentication fails or the API server returns a 403 error.
- <b>`PlanhatNotFoundError`</b>:  If the requested resource is not found.
- <b>`PlanhatServerError`</b>:  If the API server returns a 5xx error.
- <b>`PlanhatHTTPError`</b>:  If the API server returns an unspecified HTTP error.

______________________________________________________________________

### method `post`

**Source:** [`session.py:335`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L335)

```python
post(
    url: str,
    data: Any | None = None,
    json: PlanhatObject | list[PlanhatObject] | None = None,
    headers: Optional[Mapping[str, str]] = None,
    **kwargs
) → Response
```

Makes a POST request to the Planhat API.

**Args:**

- <b>`url`</b>:  The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.
- <b>`params`</b>:  The query parameters to use.
- <b>`headers`</b>:  The headers to use.
- <b>`kwargs`</b>:  Additional keyword arguments to pass to the request.

**Returns:**
The response from the Planhat API.

**Raises:**

- <b>`PlanhatAuthConfigurationError`</b>:  If the API key is not set.
- <b>`PlanhatRateLimitError`</b>:  If the API's rate limits are exceeded.
- <b>`PlanhatAuthFailedError`</b>:  If authentication fails or the API server returns a 403 error.
- <b>`PlanhatNotFoundError`</b>:  If the requested resource is not found.
- <b>`PlanhatServerError`</b>:  If the API server returns a 5xx error.
- <b>`PlanhatHTTPError`</b>:  If the API server returns an unspecified HTTP error.

______________________________________________________________________

### method `put`

**Source:** [`session.py:368`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L368)

```python
put(
    url: str,
    data: Any | None = None,
    json: PlanhatObject | list[PlanhatObject] | None = None,
    headers: Optional[Mapping[str, str]] = None,
    **kwargs
) → Response
```

Makes a PUT request to the Planhat API.

**Args:**

- <b>`url`</b>:  The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.
- <b>`params`</b>:  The query parameters to use.
- <b>`headers`</b>:  The headers to use.
- <b>`kwargs`</b>:  Additional keyword arguments to pass to the request.

**Returns:**
The response from the Planhat API.

**Raises:**

- <b>`PlanhatAuthConfigurationError`</b>:  If the API key is not set.
- <b>`PlanhatRateLimitError`</b>:  If the API's rate limits are exceeded.
- <b>`PlanhatAuthFailedError`</b>:  If authentication fails or the API server returns a 403 error.
- <b>`PlanhatNotFoundError`</b>:  If the requested resource is not found.
- <b>`PlanhatServerError`</b>:  If the API server returns a 5xx error.
- <b>`PlanhatHTTPError`</b>:  If the API server returns an unspecified HTTP error.
