<!-- markdownlint-disable -->

# module `planhat`

**Source:** [`__init__.py:0`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/__init__.py#L0)

Planhat API library for the Robocorp Python Automation Framework

This library provides an interface to the [Planhat API](https://docs.planhat.com/).  Most of the methods available in the `Planhat` are generic and can be used to make requests for all the various object endpoints (most objects have similar calls). You select the endpoint by providing a subclass of the `types.PlanhatObject` class as the `object_type` parameter.

When creating or modifying (updating/deleting) existing objects, you can initialize a new `PlanhatObject` with a dictionary of values. The dictionary keys must match the field names in the Planhat API documentation for the update or creation to be successful. Delete only requiers the correct ID.

## Variables

- **types**

______________________________________________________________________

## class `PlanhatClient`

**Source:** [`client.py:11`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L11)

Automation class to interact with the Planhat API.

For full documentation of every endpoint, refer to the [Planhat API documentation](https://docs.planhat.com).

This class provides session management and authentication including integration with the Robocorp vault as well as generic methods to interact with the Planhat API. These methods generally require you to provide the `object_type` parameter which is a subclass of `PlanhatObject`.

### method `__init__`

**Source:** [`client.py:24`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L24)

```python
__init__(
    api_key: str | None = None,
    vault_secret_name: str | None = None,
    tenant_uuid: str | None = None
) → None
```

Initializes the Planhat class. Uses the default secret vault object named `planhat_api` unless you provide authentication information via the `api_key` and `tenant_uuid` parameters or via the `vault_secret_name` parameter. If the latter is provided, the vault secret must contain the following keys:

```
    - `api_key`
    - `tenant_uuid`
```

Note: If both `api_key` and `vault_secret_name` are provided, `api_key` will be used. And, `tenant_uuid` is only required if you need to post analytics data to Planhat.

:param api_key: The Planhat API key. :param vault_secret_name: The name of the secret in the vault. :param tenant_uuid: The Planhat tenant UUID.

#### property `session`

Returns the authenticated requests session. Raises an exception if default authentication is not configured within the vault. For custom authentication, use the `authenticate` method first.

______________________________________________________________________

### method `authenticate`

**Source:** [`client.py:56`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L56)

```python
authenticate(
    api_key: str | None = None,
    vault_secret_name: str | None = None,
    tenant_uuid: str | None = None
) → None
```

Configures session authentication.

:param api_key: The Planhat API key. :param vault_secret_name: The name of the vault secret containing the Planhat API key. If you provide an API key, this parameter is ignored. The provided vaultsecret must have a key named `api_key`. Defaults to `planhat_api`.:param tenant_uuid: The Planhat tenant UUID needed to post analytics If not provided, the vault object is checked for a key named `tenant_uuid`. Ifthe key is not found, the tenant UUID is not set and analytics calls willfail.

______________________________________________________________________

### method `create_object`

**Source:** [`client.py:354`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L354)

```python
create_object(payload: PlanhatObject) → PlanhatObject
```

Creates a Planhat object. If the object already exists, a PlanhatBadRequestError is raised. Returns the newly created object.

:param payload: A PlanhatObject containing the data to create. The object must not have a Planhat ID set (e.g., `_id` in thedictionary). See the full API documentation for the requiredfields for each object type.

______________________________________________________________________

### method `delete_planhat_object`

**Source:** [`client.py:387`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L387)

```python
delete_planhat_object(payload: PlanhatObject) → Response
```

Deletes a Planhat object. If the object does not exist, a PlanhatNotFoundError is raised. You can modify this behavior by setting `ignore_errors` to `True`.

:param payload: A PlanhatObject containing the data to update. The object must have one of the following ID properties set. Theyare used in the order listed and only the first one found isused.

```
    - `id`
    - `source_id`
    - `external_id`
```

:param ignore_errors: If `True`, errors are ignored. Defaults to `False`. :returns: The response from the Planhat API.

______________________________________________________________________

### method `find_missing_objects`

**Source:** [`client.py:422`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L422)

```python
find_missing_objects(objects: PlanhatObjectList[~O]) → PlanhatObjectList[~O]
```

Finds objects missing in Planhat from the list of objects provided. The object's type and the name of the ID field must be provided. Returns those that are missing as a new Planhat Object List.

______________________________________________________________________

### method `get_object_by_id`

**Source:** [`client.py:333`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L333)

```python
get_object_by_id(
    object_type: Type[~O],
    id: str,
    id_type: PlanhatIdType | None = None
) → ~O
```

Gets a planhat object of `object_type` using the provided `id`. You can provide alternate ids via the `id_type`. If no object is found, `PlanhatNotFoundError` is raised.

:param object_type: The Planhat object type. :param id: The ID to use to find the object. :param id_type: The ID type to use. If not provided, the ID is used as-is.

______________________________________________________________________

### method `get_objects`

**Source:** [`client.py:235`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L235)

```python
get_objects(
    object_type: Type[~O],
    company_ids: str | list | None = None,
    properties: str | list | None = None
) → PlanhatObjectList[~O]
```

Gets a list of planhat objects of `object_type`.

If no objects are found, a `PlanhatNotFoundError` is raised.

You can filter the response by `company_ids`. If `company_ids` is `None`, all objects of the provided `object_type` are returned up to the maximum number of objects allowed by the Planhat API (2000 for most, 5000 for companies).

You can define the properties you'd like included using `properties`. If `properties` is `None`, only the `_id` and `name` properties are returned. If you want all properties, provide the string `ALL` to the `properties` parameter.

:param object_type: The Planhat object type. :param ids: IDs to use to filter the objects. You may provide a single ID as a string or a list of IDs. If `None`, all objects are returned.:param properties: Properties to be included in the return object. You may provide a single property as a string or a list of properties. If `None`,only the `_id` and `name` properties are returned. If you want allproperties, provide the string `ALL`.

______________________________________________________________________

### method `list_all_companies`

**Source:** [`client.py:409`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L409)

```python
list_all_companies() → PlanhatObjectList[Company]
```

Lists all companies in Planhat.

The returned objects will only include the name and ID properties.

______________________________________________________________________

### method `update_object`

**Source:** [`client.py:366`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L366)

```python
update_object(payload: PlanhatObject) → PlanhatObject
```

Updates a Planhat object. If the object does not exist, a PlanhatNotFoundError is raised.

:param payload: A PlanhatObject containing the data to update. The object must have one of the following ID properties set. Theyare used in the order listed and only the first one found isused.

```
    - `id`
    - `source_id`
    - `external_id`
```

:returns: The updated PlanhatObject.

______________________________________________________________________

### method `update_objects`

**Source:** [`client.py:201`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L201)

```python
update_objects(payload: PlanhatObjectList)
```

Bulk upserts a list of objects to Planhat. The payload must be a list of PlanhatObjects.

To decide if an object should be created or updated, Planhat first tries to match the object by one of the following keys:

```
- `_id` (Planhat native ID)
- `sourceId` (Source CRM ID)
- `externalId` (ID in your own system)
```

Note: The type of the first object in the payload is used to determine the object type. All objects in the payload must be of the same type.

:param object_type: The Planhat object type. :param payload: The PlanhatObjectList to upsert.

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
