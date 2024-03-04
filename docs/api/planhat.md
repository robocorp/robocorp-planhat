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

The `PlanhatClient` class also provides caching of objects. This means that if you retrieve a list of objects, they are stored in memory and subsequent calls to retrieve the same objects are retrieved from the cache. This can be disabled by setting the `use_caching` parameter to `False`.

Note: The Planhat API has a limit of 2000 objects per request for most object types. Companies are limited to 5000 objects per request.

**Example:**

```python
from planhat import Planhat, types

# Create a Planhat client
# Note: this will assume vault authentication
client = Planhat()

# Get a list of all companies
companies = client.get_objects(object_type=types.Company)
```

Example with custom authentication:

```python
from planhat import Planhat, types

# Create a Planhat client with custom authentication
client = Planhat(
    api_key="your_api_key",
    tenant_uuid="your_tenant_uuid"
)

# Get a list of all companies
companies = client.get_objects(object_type=types.Company)
```

### method `__init__`

**Source:** [`client.py:62`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L62)

```python
__init__(
    api_key: str | None = None,
    vault_secret_name: str | None = None,
    tenant_uuid: str | None = None,
    use_caching: bool = True
) → None
```

Initializes the Planhat class. Uses the default secret vault object named `planhat_api` unless you provide authentication information via the `api_key` and `tenant_uuid` parameters or via the `vault_secret_name` parameter. If the latter is provided, the vault secret must contain the following keys:

```
- `api_key`
- `tenant_uuid`
```

Note: If both `api_key` and `vault_secret_name` are provided, `api_key` will be used. And, `tenant_uuid` is only required if you need to post analytics data to Planhat.

**Args:**

- <b>`api_key`</b>:  The Planhat API key.
- <b>`vault_secret_name`</b>:  The name of the vault secret containing the Planhat API key. If you provide an API key, this parameter is ignored. The provided vault secret must have a key named `api_key`. Defaults to `planhat_api`.
- <b>`tenant_uuid`</b>:  The Planhat tenant UUID.
- <b>`use_caching`</b>:  If `True`, the client will cache all objects it retrieves. Defaults to `True`.

#### property `session`

The authenticated requests session.

**Returns:**

- <b>`PlanhatSession`</b>:  The authenticated requests session. Raises an exception if default authentication is not configured within the vault. For custom authentication, use the `authenticate` method first.

#### property `use_caching`

Returns the current cache setting.

If `True`, the client will cache all objects it retrieves. If `False`, the cache is disabled and all objects are retrieved from the Planhat API.

______________________________________________________________________

### method `authenticate`

**Source:** [`client.py:98`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L98)

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
- <b>`vault_secret_name`</b>:  The name of the vault secret containing the Planhat API key. If you provide an API key, this parameter is ignored. The provided vault secret must have a key named `api_key`. Defaults to `planhat_api`.
- <b>`tenant_uuid`</b>:  The Planhat tenant UUID needed to post analytics If not provided, the vault object is checked for a key named `tenant_uuid`. If the key is not found, the tenant UUID is not set and analytics calls will fail.

______________________________________________________________________

### method `create_object`

**Source:** [`client.py:606`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L606)

```python
create_object(payload: PlanhatObject) → PlanhatObject
```

Creates a Planhat object.

**Args:**

- <b>`payload`</b>:  A PlanhatObject containing the data to create. The object must not have a Planhat ID set and must have the required fields for the object type. See the Planhat API documentation for more information.

**Returns:**
The newly created PlanhatObject.

**Raises:**

- <b>`PlanhatBadRequestError`</b>:  If the object already exists.

**Example:**

```python
# Create a new company
new_company = types.Company(name="New Company")
created_company = client.create_object(new_company)
```

______________________________________________________________________

### method `delete_planhat_object`

**Source:** [`client.py:682`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L682)

```python
delete_planhat_object(payload: PlanhatObject) → Response
```

Deletes a Planhat object.

If the object does not exist, a PlanhatNotFoundError is raised. This behavior can be modified by setting `ignore_errors` to `True`.

**Args:**

- <b>`payload`</b>:  A PlanhatObject containing the data to update. The object must have one of the ID properties set. They are used in the order listed and only the first one found is used. These properties include `id`, `source_id`, and `external_id`.
- <b>`ignore_errors`</b>:  If `True`, errors are ignored. Defaults to `False`.

**Returns:**
The response from the Planhat API.

**Raises:**

- <b>`PlanhatNotFoundError`</b>:  If the object does not exist.

**Example:**

```python
# Delete a company
company = client.get_object_by_id(object_type=types.Company, id="1")
client.delete_planhat_object(company)
```

______________________________________________________________________

### method `find_missing_objects`

**Source:** [`client.py:735`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L735)

```python
find_missing_objects(objects: PlanhatObjectList[~P]) → PlanhatObjectList[~P]
```

Finds objects missing in Planhat from the list of objects provided.

The object's type and the name of the ID field must be provided. This method returns those that are missing as a new Planhat Object List.

**Args:**

- <b>`objects`</b>:  List of objects to check.

**Returns:**
A new Planhat Object List containing the missing objects.

**Example:**

```python
# Find missing companies
companies = types.Company.from_list([
    {"externalId": "test-002", "name": "Test Company 2"},
    {"externalId": "test-003", "name": "Test Company 3"}
])
missing_companies = client.find_missing_objects(companies)

# You could then create the missing companies, for example
client.create_objects(missing_companies)
```

______________________________________________________________________

### method `get_object_by_id`

**Source:** [`client.py:558`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L558)

```python
get_object_by_id(
    object_type: Type[~P],
    id: str,
    id_type: PlanhatIdType | None = None
) → ~P
```

Gets a planhat object of `object_type` using the provided `id`.

You can provide alternate ids via the `id_type`. If no object is found, `PlanhatNotFoundError` is raised. This method respects the `use_caching` setting and will use the cache if enabled.

**Args:**

- <b>`object_type`</b>:  The Planhat object type.
- <b>`id`</b>:  The ID to use to find the object.
- <b>`id_type`</b>:  The ID type to use. If not provided, the ID is used as-is.

**Returns:**
The planhat object of `object_type` that matches the provided `id`.

**Raises:**

- <b>`ValueError`</b>:  If the object type is not valid.
- <b>`PlanhatNotFoundError`</b>:  If no object is found.

**Example:**

```python
# Get a company by its ID
company = client.get_object_by_id(object_type=types.Company, id="1")

# Get a company by its source ID
company = client.get_object_by_id(
    object_type=types.Company,
    id="1",
    id_type=types.PlanhatIdType.SOURCE_ID,
)
```

______________________________________________________________________

### method `get_objects`

**Source:** [`client.py:462`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L462)

```python
get_objects(object_type, company_ids=None, properties=None)
```

Gets a list of planhat objects of `object_type`.

This keyword respects the `use_caching` setting and will use the cache if enabled, unless the `properties` parameter is provided.

If no objects are found, a `PlanhatNotFoundError` is raised.

You can filter the response by `company_ids`. If `company_ids` is `None`, all objects of the provided `object_type` are returned up to the maximum number of objects allowed by the Planhat API (2000 for most, 5000 for companies).

You can define the properties you'd like included using `properties`. If `properties` is `None`, only the `_id` and `name` properties are returned (or whatever properties are attached to the object in the cache). If you want all properties, provide the string `ALL` to the `properties` parameter.

**Args:**

- <b>`object_type`</b>:  The Planhat object type.
- <b>`company_ids`</b>:  IDs to use to filter the objects. You may provide a single ID as a string or a list of IDs. If `None`, all objects are returned.
- <b>`properties`</b>:  Properties to be included in the return object. You may provide a single property as a string or a list of properties. If `None`, only the `_id` and `name` properties are returned. If you want all properties, provide the string `ALL`.

**Returns:**
A list of planhat objects of `object_type` that match the provided filters.

**Raises:**

- <b>`ValueError`</b>:  If the object type is not valid.
- <b>`PlanhatNotFoundError`</b>:  If no objects are found.

**Example:**

```python
# Get all companies
companies = client.get_objects(object_type=types.Company)

# Get all companies with the provided IDs
companies = client.get_objects(object_type=types.Company, company_ids=["1", "2"])

# Get all companies with the provided IDs and properties
companies = client.get_objects(
    object_type=types.Company,
    company_ids=["1", "2"],
    properties=["name", "industry"]
)
```

______________________________________________________________________

### method `list_all_companies`

**Source:** [`client.py:715`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L715)

```python
list_all_companies() → PlanhatObjectList[Company]
```

Lists all companies in Planhat using the lean companies endpoint.

This endpoint returns only the company name and ID. This method does not respect the `use_caching` setting and always retrieves the objects from the API. Note that this endpoint is not restricted to the usual 5000 company limit.

**Returns:**
A list of all companies in Planhat with only the company name and ID.

______________________________________________________________________

### method `update_object`

**Source:** [`client.py:635`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L635)

```python
update_object(payload: PlanhatObject) → PlanhatObject
```

Updates a Planhat object.

When updating an object, you must provide the object with the updated values. The object must have one of the ID properties set. They are used in the order listed and only the first one found is used. These properties include `id`, `source_id`, and `external_id`. Certain properties may not be updated via the API, those properties should be removed or never selected when retrieving the object.

**Args:**

- <b>`payload`</b>:  A PlanhatObject containing the data to update. The object must have one of the ID properties set. They are used in the order listed and only the first one found is used.

  ```
   - `id`
   - `source_id`
   - `external_id`
  ```

**Returns:**
The updated PlanhatObject.

**Raises:**

- <b>`PlanhatNotFoundError`</b>:  If the object does not exist.

**Example:**

```python
# Update a company, select only the properties you want to update
company = client.get_object_by_id(
    object_type=types.Company,
    id="1",
    properties=["name"],
)
company.name = "Updated Company"
updated_company = client.update_object(company)
```

______________________________________________________________________

### method `update_objects`

**Source:** [`client.py:298`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/client.py#L298)

```python
update_objects(payload: PlanhatObjectList[~P]) → dict | list[dict]
```

Bulk upserts a list of objects to Planhat.

To decide if an object should be created or updated, Planhat first tries to match the object by one of the following keys:

```
- `_id` (Planhat native ID)
- `sourceId` (Source CRM ID)
- `externalId` (ID in your own system)
```

Note: The type of the first object in the payload is used to determine the object type. All objects in the payload must be of the same type.

When updating an object, certain properties may not be updated via the API, those properties should be removed or never selected when retrieving the object.

**Args:**

- <b>`payload`</b>:  The PlanhatObjectList to upsert.

**Returns:**
If the length of the payload is greater than 5000, the functionreturns a list of batched responses. Otherwise, it returns asingle response. The response is a dictionary containing thenumber of objects created and updated, for example:

{

- <b>`"created"`</b>:  2,
- <b>`"createdErrors"`</b>:  \[\],
- <b>`"insertsKeys"`</b>:  \[ {
- <b>`"_id"`</b>:  "623a1906b4c82d7a1ac76224",
- <b>`"externalId"`</b>:  "test-002"},{
- <b>`"_id"`</b>:  "623a1906b4c82d7a1ac76225",
- <b>`"externalId"`</b>:  "test-003"},...\],
- <b>`"updated"`</b>:  0,
- <b>`"updatedErrors"`</b>:  \[\],
- <b>`"updatesKeys"`</b>:  \[\],
- <b>`"nonupdates"`</b>:  0,
- <b>`"modified"`</b>:  \[\],
- <b>`"upsertedIds"`</b>:  \[ "623a1906b4c82d7a1ac76224", "623a1906b4c82d7a1ac76225", ...\],
- <b>`"permissionErrors"`</b>:  \[\]}

**Example:**

```python
updated_objects = types.Company.from_list([
    {"externalId": "test-002", "name": "Test Company 2"},
    {"externalId": "test-003", "name": "Test Company 3"}
])
response = client.update_objects(updated_objects)
```

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
