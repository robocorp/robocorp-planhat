<!-- markdownlint-disable -->

# module `planhat.types`

**Source:** [`types.py:0`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L0)

Data types used in the Planhat client.

______________________________________________________________________

## enum `PlanhatIdType`

**Source:** [`types.py:23`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L23)

### Values

- **PLANHAT_ID** =
- **SOURCE_ID** = srcid-
- **EXTERNAL_ID** = extid-

______________________________________________________________________

## class `DateTimeEncoder`

**Source:** [`types.py:29`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L29)

A custom JSON encoder for use with Planhat objects.

______________________________________________________________________

### method `default`

**Source:** [`types.py:32`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L32)

```python
default(obj: Any) → Any
```

Returns a JSON-serializable version of the provided object.

______________________________________________________________________

## class `PlanhatObject`

**Source:** [`types.py:42`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L42)

A base Planhat object. This is a dictionary with some additional functionality.

The dictionary is the JSON response from Planhat or a dictionary containing the Planhat object.

The class includes several class methods to facilitate creation of objects from API responses or lists of dictionaries. It also includes methods to facilitate encoding the object as a JSON string for API requests.

When creating objects using dictionaries, you must use the keys that Planhat uses in its API responses. For example, the key for the Planhat ID is "\_id". See Planhat API documentation for more information.

Example usage:

from planhat import PlanhatObject

# Create a Planhat object from a dictionarydata = {"\_id": "123","name": "Company A"}company = PlanhatObject(data)

# Create a Planhat object from an API responseresponse = requests.get("https://api.planhat.com/companies/123")company = PlanhatObject.from_response(response)

# Create a Planhat object from a list of dictionariesdata = \[{"\_id": "123","name": "Company A"},{"\_id": "456","name": "Company B"}\]companies = PlanhatObject.from_list(data)

### method `__init__`

**Source:** [`types.py:208`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L208)

```python
__init__(
    data: dict | None = None,
    id: str | None = None,
    source_id: str | None = None,
    external_id: str | None = None,
    custom: dict | None = None
)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

**Args:**

- <b>`data`</b>:  A dictionary containing the Planhat object. If provided, all other parameters are ignored.
- <b>`id`</b>:  The Planhat ID of the object.
- <b>`source_id`</b>:  The source ID of the object.
- <b>`external_id`</b>:  The external ID of the object.
- <b>`custom`</b>:  A dictionary containing custom fields for the object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `NamedObjectMixin`

**Source:** [`types.py:380`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L380)

### method `__init__`

**Source:** [`types.py:381`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L381)

```python
__init__(*args, name: str | None = None, **kwargs)
```

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `name`

The name of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Company`

**Source:** [`types.py:402`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L402)

Class to represent Companies ("accounts"), which are your customers.

Depending on your business these might be agencies, schools, other businesses or something else. Companies can also be your previous customers and potentially future customers (prospects).

The company object is one of the most central in Planhat since most other objects relate to it, and it's frequently used to filter out other information, such as endsuers, licenses, notes etc.

In Planhat it is possible have a hierarchical structure for the companies, meaning that they can be grouped into organizations with parents and children in a tree like structure.

### method `__init__`

**Source:** [`types.py:381`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L381)

```python
__init__(*args, name: str | None = None, **kwargs)
```

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `name`

The name of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `PlanhatCompanyOwnedObject`

**Source:** [`types.py:421`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L421)

An abstract class representing objects that are owned by a company.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Asset`

**Source:** [`types.py:456`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L456)

Assets in Planhat can represent many different things depending on your use case. It could be drones, if you're selling a drone tracking product, or it could be instances of your product in cases where a single customer can run multiple instances of your product in parallel. Assets could also represent your different products.

More generally, Assets are "nested objects" for which you may want to track usage separately, but don't need to treat them as separate customers with individual contacts, conversations, etc.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Campaign`

**Source:** [`types.py:472`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L472)

Manage campaigns you are running inside companies, e.g., to drive adoption or to deepen stakeholder relations.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Churn`

**Source:** [`types.py:483`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L483)

Each time one of your customers churns or downgrades you can add a specific log about this. Mostly this "churn log" is added manually by the CSM from within Planhat, but there may also be times when you want to add it over API, for example if you're capturing information about downgrades and churn natively in-app in your own platform and want to send that over to Planhat.

The churn logs in Planhat typically contain the reasons for the churn, the value, date etc. It's important to note though that it doesn't affect actual revenue numbers and KPIs such as churn rate, renewal rate etc, on it's own. Those calculations are entirely based on underlying license data.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Conversation`

**Source:** [`types.py:503`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L503)

Represents conversations of different types.

This class represents conversations of various types such as email, chat, support tickets, and manually logged notes. Custom types can also be created in Planhat to represent things such as "in person meeting", "Training" etc. The default types (email, chat, ticket, call) are reserved and should not be created over API.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `CustomField`

**Source:** [`types.py:519`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L519)

Represents custom fields in Planhat.

Most objects in Planhat can be customized by creating your own custom fields. The parent property indicates which model a given custom field belongs to. Typically, custom fields are created from within the Planhat app. However, in some special cases, managing over API may be more convenient.

### method `__init__`

**Source:** [`types.py:534`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L534)

```python
__init__(*args, parent: str | None = None, **kwargs)
```

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `parent`

The singular name of the parent model which owns this custom field

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Enduser`

**Source:** [`types.py:549`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L549)

Represents an individual at one of your customers. This could be a user of your product, a business contact or both. Endusers can be created automatically based on user tracking events, or based on conversations such as emails and tickets.

Often, automatic creation of contacts along with sync from an external CRM or similar is enough. But there are also situations where you may want to be 100% sure all your users exist in Planhat, and then it would make sense to create them in Planhat over API as soon as they get created in your own system.

If 'companyId' is not present in the payload, and the email has a domain already registered within a company, then Planhat will auto-assign the new enduser to the company using domain matching.

### method `__init__`

**Source:** [`types.py:571`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L571)

```python
__init__(*args, email: str | None = None, **kwargs)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `email`

The email address of the enduser.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Invoice`

**Source:** [`types.py:586`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L586)

Represents Invoices in Planhat.

Invoices are normally generated automatically in Planhat when a license is created or renewed. Each invoice can include multiple line items. However, Planhat does not prepare invoices that can be sent to customers. They are primarily meant to help anyone working with your customers to know the status of current and past invoicing.

**Note:**

> The default date fields format for invoices should be in integer days format (Days since January 1, 1970, Unix epoch).

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Issue`

**Source:** [`types.py:606`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L606)

Issues typically represent Bugs or Feature Requests. Many of our customers fetch issues from Jira, but they can also be pushed to Planhat from other product management tools such as Product Board or Aha! You can also manage issues directly in Planhat without any external tool. Just keep in mind that the functionality is basic and mostly intended to contribute to the customer 360 view.

Issues in Planhat can link to multiple companies, to multiple endusers and to multiple conversations.

### method `__init__`

**Source:** [`types.py:623`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L623)

```python
__init__(
    *args,
    company_ids: list[str] | None = None,
    company_names: list[str] | None = None,
    enduser_ids: list[str] | None = None,
    enduser_names: list[str] | None = None,
    **kwargs
)
```

#### property `company_ids`

The IDs of the companies that this issue is linked to.

#### property `company_names`

The names of the companies that this issue is linked to.

#### property `custom`

Returns the custom fields of the object.

#### property `enduser_ids`

The IDs of the endusers that this issue is linked to.

#### property `enduser_names`

The names of the endusers that this issue is linked to.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `License`

**Source:** [`types.py:679`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L679)

Represents your customers' subscriptions to your service. This is the base for MRR (or ARR) calculations and most revenue reports. For non-recurring revenue, refer to the Sale (NRR) object. There are many ways to get license data into Planhat including incoming webhooks and CRM integrations. In some cases, handling it over the API is preferred, for example if the main source of license data is your own system.

Licenses in Planhat can be fixed period with a defined start and end date, or they can be non-fixed period (sometimes called open-ended or evergreen). Open-ended licenses initially don't have a specified end date since the customer may cancel at any time. Once the license is churned/lost, non-fixed period licenses can also have an end date.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Note`

**Source:** [`types.py:700`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L700)

Notes in Planhat are technically Conversations. You can create your own custom Touch Types to easily distinguish between different types of notes. You can also use custom fields to add more nuance to your Notes.

It's quite common for Notes in Planhat to sync with external systems such as Salesforce, Notes can also be created via Zapier or Planhats's native incoming webhooks.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `NPS`

**Source:** [`types.py:714`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L714)

Represents the individual responses to an NPS survey in Planhat. These are typically created automatically when running an NPS campaign in Planhat, or sometimes imported from external NPS tools. A single enduser/contact can have multiple records if they responded to different surveys over time.

Based on the NPS records, each enduser and company in Planhat also get an NPS score assigned.

### method `__init__`

**Source:** [`types.py:729`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L729)

```python
__init__(*args, campaign_id: str | None = None, **kwargs)
```

#### property `campaign_id`

The ID of the campaign that this NPS record is linked to.

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Opportunity`

**Source:** [`types.py:744`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L744)

Represents a sales opportunity in Planhat. This could be a chance to sell to a new customer or more commonly, an opportunity to expand an existing account.

**Note:**

> Opportunities are not the same as Licenses. However, when an opportunity is closed won in Planhat, there is an optional setting to generate a license based on the opportunity data.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Objective`

**Source:** [`types.py:760`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L760)

Represents the objectives and their health in Planhat.

This class is critical for tracking objectives and the health per objective.

Pro-tip: use your average Objective health in the Health Score!

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Project`

**Source:** [`types.py:774`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L774)

Represents Projects in Planhat.

Projects can represent many different real world objects with a natural start and stop date. For example, a service provider for schools may use Projects to represent classes or courses. If you're selling a software to run sales competitions, then each competition may be a project.

Using custom fields, projects can be tailored to specific needs. Just like Assets, usage data and time series data (metrics) can be associated with your Projects.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Sale`

**Source:** [`types.py:793`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L793)

The Sale (NRR) model represents not recurring revenue, like an onboarding fee, or a one-off professional services project.

### method `__init__`

**Source:** [`types.py:424`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L424)

```python
__init__(
    *args,
    company_id: str | None = None,
    company_name: str | None = None,
    **kwargs
)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Task`

**Source:** [`types.py:804`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L804)

Represents tasks in Planhat. Tasks are future actions, which can be simple "to-do" items without a specific due date, reminders for a specific time, or meetings with a start and end time.

Most tasks are automatically generated in Planhat based on set rules. They can also be steps in a Playbook or created ad-hoc like in any task management app.

Tasks managed over the API should typically have the mainType property set to `task`. Another potential value is `event`, indicating a sync to or from a calendar like Google Calendar. Tasks of type `event` can also be created in Planhat without syncing them back to any calendar.

Once a task is completed, it's archived and generally not visible in Planhat anymore. Sometimes, when completing a task like a training session, a note summarizing how it went is logged. This is managed automatically by Planhat when working in the Planhat app.

### method `__init__`

**Source:** [`types.py:829`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L829)

```python
__init__(*args, task_type: str | None = None, **kwargs)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

#### property `task_type`

The type of task that this task is.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Ticket`

**Source:** [`types.py:844`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L844)

Tickets in Planhat are Conversations. If you plan to send tickets to Planhat via API, you can also use that endpoint. The ticket endpoint contains convenience logic for saving tickets specifically, like setting the proper type automatically.

Most customers sync tickets from an external system like Zendesk or Salesforce. If your ticketing system isn't natively supported or you have your own system, please let us know. We'll be happy to discuss how to best work with this API.

### method `__init__`

**Source:** [`types.py:861`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L861)

```python
__init__(*args, email: str | None = None, **kwargs)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `email`

The email address of user who submitted the ticket.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `User`

**Source:** [`types.py:876`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L876)

Represents a User in Planhat.

Users are all your team members that need access to Planhat. Users can be created in the app, using spreadsheet upload or over API. If you're using teams to group your users in Planhat you'll need to call a separate endpoint to associate your Users with the right teams.

If a user is flagged as inactive, they will not be able to login to Planhat and they will not get notifications, but they will be available for assigning accounts etc.

### method `__init__`

**Source:** [`types.py:894`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L894)

```python
__init__(
    *args,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    **kwargs
)
```

#### property `custom`

Returns the custom fields of the object.

#### property `email`

The email address of the user.

#### property `external_id`

Returns the external ID of the object.

#### property `first_name`

The first name of the user.

#### property `id`

Returns the Planhat ID of the object.

#### property `last_name`

The last name of the user.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Workspace`

**Source:** [`types.py:938`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L938)

If you work with sub-instances at your customers, e.g., connecting with different departments or with different versions of your product (think like a Workspace in Slack), then this is the object to track that engagement!

### method `__init__`

**Source:** [`types.py:950`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L950)

```python
__init__(*args, name: str | None = None, **kwargs)
```

#### property `company_id`

The ID of the company that owns this object.

#### property `company_name`

The name of the company that owns this object.

#### property `custom`

Returns the custom fields of the object.

#### property `external_id`

Returns the external ID of the object.

#### property `id`

Returns the Planhat ID of the object.

#### property `name`

The name of the workspace.

#### property `response`

Returns the response from Planhat which originated this object.

#### property `source_id`

Returns the source ID of the object.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:365`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L365)

```python
encode() → bytes
```

Encodes and returns  the object as a byte-like JSON string for API body payloads.

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:189`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L189)

```python
from_list(data: list[dict]) → PlanhatObjectList[P]
```

Creates a PlanhatList from a list of dictionaries.

**Args:**

- <b>`data`</b>:  A list of dictionaries representing Planhat objects. The keys must match the Planhat API endpoint keys.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:94`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L94)

```python
from_response(response: Response) → P | PlanhatObjectList[P]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

**Args:**

- <b>`response`</b>:  The response from Planhat.

**Returns:**
A Planhat object or list of Planhat objects.

**Raises:**

- <b>`TypeError`</b>:  If the response from Planhat is not dictionary- or list-like.

______________________________________________________________________

### classmethod `get_type_urlpath`

**Source:** [`types.py:203`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L203)

```python
get_type_urlpath() → str
```

Returns the URL path for the the object type.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:320`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L320)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

**Args:**

- <b>`id_type`</b>:  The ID type to use when generating the URL path.

**Returns:**
The URL path for the object.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object by by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

```python
to_serializable_json() → dict
```

Returns a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `PlanhatObjectList`

**Source:** [`types.py:965`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L965)

A list of Planhat objects.

### method `__init__`

**Source:** [`types.py:968`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L968)

```python
__init__(_PlanhatObjectList__iterable: Optional[Iterable[~P]] = None) → None
```

Initializes the Planhat list using the provided list of Planhat objects. The type of the first object in the list is used to determine the type of the list.

**Args:**

- <b>`__iterable`</b>:  A list of Planhat objects.

______________________________________________________________________

### method `append`

**Source:** [`types.py:1119`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1119)

```python
append(obj: ~P) → None
```

Appends a Planhat object to the list.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:1312`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1312)

```python
encode() → bytes
```

Encodes the list as a byte-like JSON string for API body payloads

______________________________________________________________________

### method `extend`

**Source:** [`types.py:1126`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1126)

```python
extend(objs: Iterable[~P]) → None
```

Extends the list with a list of Planhat objects.

______________________________________________________________________

### method `find_by_company_id`

**Source:** [`types.py:1273`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1273)

```python
find_by_company_id(company_id: str) → PlanhatObjectList[P]
```

Returns the Planhat objects associated with the provided company ID.

**Args:**

- <b>`company_id`</b>:  The ID of the company.

**Returns:**
A list of Planhat objects associated with the given company ID.

______________________________________________________________________

### method `find_by_external_id`

**Source:** [`types.py:1224`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1224)

```python
find_by_external_id(external_id: str) → ~P
```

Retrieves the Planhat objects using the provided external ID.

**Args:**

- <b>`external_id`</b>:  The external ID of the Planhat object to retrieve.

**Returns:**
The Planhat object with the provided external ID.

**Raises:**

- <b>`PlanhatNotFoundError`</b>:  If no Planhat object with the provided external ID is found.

______________________________________________________________________

### method `find_by_id`

**Source:** [`types.py:1175`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1175)

```python
find_by_id(id: str) → ~P
```

Retrieves the Planhat object using the provided ID.

**Args:**

- <b>`id`</b>:  The ID of the Planhat object to retrieve.

**Returns:**
The Planhat object with the provided ID.

**Raises:**

- <b>`PlanhatNotFoundError`</b>:  If no Planhat object with the provided ID is found.

______________________________________________________________________

### method `find_by_id_type`

**Source:** [`types.py:1249`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1249)

```python
find_by_id_type(id: str, id_type: PlanhatIdType | None = None) → ~P
```

Returns the Planhat object based on the provided ID and ID type.

**Args:**

- <b>`id`</b>:  The ID of the Planhat object to retrieve.
- <b>`id_type`</b>:  The type of the ID. If None, defaults to PlanhatIdType.PLANHAT_ID.

**Returns:**
The Planhat object with the provided ID.

**Raises:**

- <b>`ValueError`</b>:  If an invalid ID type is provided.
- <b>`PlanhatNotFoundError`</b>:  If no Planhat object with the provided ID is found.

______________________________________________________________________

### method `find_by_source_id`

**Source:** [`types.py:1199`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1199)

```python
find_by_source_id(source_id: str) → ~P
```

Returns the Planhat objects with the provided source ID.

**Args:**

- <b>`source_id`</b>:  The source ID of the Planhat object to retrieve.

**Returns:**
The Planhat object with the provided source ID.

**Raises:**

- <b>`PlanhatNotFoundError`</b>:  If no Planhat object with the provided source ID is found.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:1325`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1325)

```python
get_urlpath() → str
```

Returns the URL path for object type of the list.

______________________________________________________________________

### method `insert`

**Source:** [`types.py:1132`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1132)

```python
insert(index: SupportsIndex, obj: ~P) → None
```

Inserts a Planhat object at the provided index.

______________________________________________________________________

### method `is_obj_in_list`

**Source:** [`types.py:1155`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1155)

```python
is_obj_in_list(obj: ~P) → bool
```

Checks if the provided Planhat object is in the list based on IDs.

**Args:**

- <b>`obj`</b>:  The Planhat object to check.

**Returns:**
True if the object is in the list, False otherwise.

**Raises:**

- <b>`TypeError`</b>:  If the provided object is not of the expected type.

______________________________________________________________________

### method `remove`

**Source:** [`types.py:1140`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1140)

```python
remove(obj: ~P) → None
```

Removes the first occurance of the provided Planhat object from the list.

**Args:**

- <b>`obj`</b>:  The Planhat object to remove from the list.

**Raises:**

- <b>`TypeError`</b>:  If the provided object is not of the expected type.
- <b>`ValueError`</b>:  If the provided object is not in the list.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:1318`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L1318)

```python
to_serializable_json() → list[dict]
```

Return a list of dictionaries where all `datetime` objects within the objects are converted to ISO 8601 strings.
