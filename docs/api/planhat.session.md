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

**Source:** [`session.py:34`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L34)

Attaches HTTP Authorization to the given Request object.

### method `__init__`

**Source:** [`session.py:37`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L37)

```python
__init__(api_key: str) → None
```

______________________________________________________________________

## class `PlanhatSession`

**Source:** [`session.py:46`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L46)

A Planhat session.

### method `__init__`

**Source:** [`session.py:49`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L49)

```python
__init__(
    api_key: str | None = None,
    vault_secret_name: str | None = None,
    tenant_uuid: str | None = None
)
```

Initializes the Planhat session. If you want to use a non-default secret or provide the API key directly, you can do so by providing the `api_key` and `vault_secret_name` parameters, otherwise the default vault secret `planhat_api` is used.

______________________________________________________________________

### method `authenticate`

**Source:** [`session.py:82`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L82)

```python
authenticate(
    api_key: str | None = None,
    vault_secret_name: str | None = None,
    tenant_uuid: str | None = None
) → None
```

Configures session authentication.

:param api_key: The Planhat API key. :param vault_secret_name: The name of the vault secret containing the Planhat API key. If you provide an API key, this parameter is ignored. The provided vaultsecret must have a key named `api_key`. It may also have a key names`tenant_uuid` which is used for analytics calls.:param tenant_uuid: The Planhat tenant UUID needed to post analytics If not provided, the vault object is checked for a key named `tenant_uuid`. Ifthe key is not found, the tenant UUID is not set and analytics calls willfail.

______________________________________________________________________

### method `create_analytics`

**Source:** [`session.py:376`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L376)

```python
create_analytics(activity: dict[str, Any], **kwargs: Any) → Response
```

Creates an activity in Planhat.

:param activity: The activity to create. :param kwargs: Additional keyword arguments to pass to the request. :return: The response from the Planhat API.

______________________________________________________________________

### method `create_bulk_activities`

**Source:** [`session.py:389`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L389)

```python
create_bulk_activities(
    activities: list[dict[str, Any]],
    **kwargs: Any
) → Response
```

Creates a bulk of activities in Planhat.

:param activities: The activities to create. :param kwargs: Additional keyword arguments to pass to the request. :return: The response from the Planhat API.

______________________________________________________________________

### method `delete`

**Source:** [`session.py:324`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L324)

```python
delete(
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    **kwargs: Any
) → Response
```

Makes a DELETE request to the Planhat API.

:param url: The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.:param params: The query parameters to use. :param headers: The headers to use. :param kwargs: Additional keyword arguments to pass to the request. :return: The response from the Planhat API.

______________________________________________________________________

### method `get`

**Source:** [`session.py:240`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L240)

```python
get(
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    **kwargs: Any
) → Response
```

Makes a GET request to the Planhat API.

:param url: The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.:param params: The query parameters to use. :param headers: The headers to use. :param kwargs: Additional keyword arguments to pass to the request. :return: The response from the Planhat API.

______________________________________________________________________

### method `patch`

**Source:** [`session.py:302`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L302)

```python
patch(
    url: str,
    data: Any | None = None,
    json: PlanhatObject | list[PlanhatObject] | None = None,
    headers: dict | None = None,
    **kwargs: Any
) → Response
```

Makes a PATCH request to the Planhat API.

:param url: The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.:param data: The data to send in the request body. :param json: The JSON data to send in the request body. :param headers: The headers to use. :param kwargs: Additional keyword arguments to pass to the request. :return: The response from the Planhat API.

______________________________________________________________________

### method `post`

**Source:** [`session.py:258`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L258)

```python
post(
    url: str,
    data: Any | None = None,
    json: PlanhatObject | list[PlanhatObject] | None = None,
    headers: dict | None = None,
    **kwargs: Any
) → Response
```

Makes a POST request to the Planhat API.

:param url: The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.:param data: The data to send in the request body. :param json: The JSON data to send in the request body. :param headers: The headers to use. :param kwargs: Additional keyword arguments to pass to the request. :return: The response from the Planhat API.

______________________________________________________________________

### method `put`

**Source:** [`session.py:280`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/session.py#L280)

```python
put(
    url: str,
    data: Any | None = None,
    json: PlanhatObject | list[PlanhatObject] | None = None,
    headers: dict | None = None,
    **kwargs: Any
) → Response
```

Makes a PUT request to the Planhat API.

:param url: The URL to make the request to. If the URL does not start with `http`, the URL is appended to the Planhat API host.:param data: The data to send in the request body. :param json: The JSON data to send in the request body. :param headers: The headers to use. :param kwargs: Additional keyword arguments to pass to the request. :return: The response from the Planhat API.
