<!-- markdownlint-disable -->

# module `planhat.errors`

**Source:** [`errors.py:0`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L0)

______________________________________________________________________

## exception `PlanhatError`

**Source:** [`errors.py:6`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L6)

Base class for all Planhat API errors.

______________________________________________________________________

## exception `PlanhatHTTPError`

**Source:** [`errors.py:10`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L10)

Base class for all Planhat API Session errors.

### method `__init__`

**Source:** [`errors.py:13`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L13)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatAuthConfigurationError`

**Source:** [`errors.py:22`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L22)

Error when authentication is not configured correctly.

______________________________________________________________________

## exception `PlanhatAuthFailedError`

**Source:** [`errors.py:26`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L26)

Error when authentication fails or the API server returns a 403 error.

### method `__init__`

**Source:** [`errors.py:13`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L13)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatRateLimitError`

**Source:** [`errors.py:30`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L30)

Error when the API's rate limits are exceeded.

### method `__init__`

**Source:** [`errors.py:13`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L13)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatNotFoundError`

**Source:** [`errors.py:34`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L34)

Error when the requested resource is not found.

### method `__init__`

**Source:** [`errors.py:13`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L13)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatServerError`

**Source:** [`errors.py:38`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L38)

Error when the API server returns a 5xx error.

### method `__init__`

**Source:** [`errors.py:13`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L13)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatBadRequestError`

**Source:** [`errors.py:42`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L42)

Error when the API server returns a 400 error.

### method `__init__`

**Source:** [`errors.py:13`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L13)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```
