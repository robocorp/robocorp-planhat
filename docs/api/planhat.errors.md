<!-- markdownlint-disable -->

# module `planhat.errors`

**Source:** [`errors.py:0`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L0)

______________________________________________________________________

## exception `PlanhatError`

**Source:** [`errors.py:4`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L4)

Base class for all Planhat API errors.

______________________________________________________________________

## exception `PlanhatHTTPError`

**Source:** [`errors.py:8`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L8)

Base class for all Planhat API Session errors.

### method `__init__`

**Source:** [`errors.py:11`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L11)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatAuthConfigurationError`

**Source:** [`errors.py:20`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L20)

Error when authentication is not configured correctly.

______________________________________________________________________

## exception `PlanhatAuthFailedError`

**Source:** [`errors.py:24`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L24)

Error when authentication fails or the API server returns a 403 error.

### method `__init__`

**Source:** [`errors.py:11`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L11)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatRateLimitError`

**Source:** [`errors.py:28`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L28)

Error when the API's rate limits are exceeded.

### method `__init__`

**Source:** [`errors.py:11`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L11)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatNotFoundError`

**Source:** [`errors.py:32`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L32)

Error when the requested resource is not found.

### method `__init__`

**Source:** [`errors.py:11`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L11)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatServerError`

**Source:** [`errors.py:36`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L36)

Error when the API server returns a 5xx error.

### method `__init__`

**Source:** [`errors.py:11`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L11)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```

______________________________________________________________________

## exception `PlanhatBadRequestError`

**Source:** [`errors.py:40`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L40)

Error when the API server returns a 400 error.

### method `__init__`

**Source:** [`errors.py:11`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/errors.py#L11)

```python
__init__(message: str | None = None, code: str | None = None, *args, **kwargs)
```
