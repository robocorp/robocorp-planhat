<!-- markdownlint-disable -->

# module `planhat.types`

**Source:** [`types.py:0`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L0)

Data types used in the Planhat client.

______________________________________________________________________

## enum `PlanhatIdType`

**Source:** [`types.py:22`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L22)

### Values

- **PLANHAT_ID** =
- **SOURCE_ID** = srcid-
- **EXTERNAL_ID** = ext-

______________________________________________________________________

## class `DateTimeEncoder`

**Source:** [`types.py:28`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L28)

A custom JSON encoder for use with Planhat objects.

______________________________________________________________________

### method `default`

**Source:** [`types.py:31`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L31)

```python
default(obj: Any) → Any
```

Returns a JSON-serializable version of the provided object.

______________________________________________________________________

## class `PlanhatObject`

**Source:** [`types.py:41`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L41)

A base Planhat object. This is a dictionary with some additional functionality. The dictionary is the JSON response from Planhat or a dictionary containing the Planhat object.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `NamedObjectMixin`

**Source:** [`types.py:247`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L247)

An abstract class representing objects that have a name.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Company`

**Source:** [`types.py:262`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L262)

Companies ("accounts"), are your customers. Depending on your business these might be agencies, schools, other businesses or something else. Companies can also be your previous customers and potentially future customers (prospects).

The company object is one of the most central in Planhat since most other objects relate to it, and it's frequently used to filter out other information, such as endsuers, licenses, notes etc.

In Planhat it is possible have a hierarchical structure for the companies, meaning that they can be grouped into organizations with parents and children in a tree like structure.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `PlanhatCompanyOwnedObject`

**Source:** [`types.py:275`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L275)

An abstract class representing objects that are owned by a company.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Asset`

**Source:** [`types.py:289`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L289)

Assets in Planhat can represent many different things depending on your use case. It could be drones, if you're selling a drone tracking product, or it could be instances of your product in cases where a single customer can run multiple instances of your product in parallel. Assets could also represent your different products.

More generally, Assets are "nested objects" for which you may want to track usage separately, but don't need to treat them as separate customers with individual contacts, conversations, etc.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Campaign`

**Source:** [`types.py:300`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L300)

Manage campaigns you are running inside companies, e.g., to drive adoption or to deepen stakeholder relations.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Churn`

**Source:** [`types.py:308`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L308)

Each time one of your customers churns or downgrades you can add a specific log about this. Mostly this "churn log" is added manually by the CSM from within Planhat, but there may also be times when you want to add it over API, for example if you're capturing information about downgrades and churn natively in-app in your own platform and want to send that over to Planhat.

The churn logs in Planhat typically contain the reasons for the churn, the value, date etc. It's important to note though that it doesn't affect actual revenue numbers and KPIs such as churn rate, renewal rate etc, on it's own. Those calculations are entirely based on underlying license data.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Conversation`

**Source:** [`types.py:319`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L319)

Conversations can be of different types such as email, chat, support tickets and manually logged notes. You can also create your own types in Planhat to represent things such as "in person meeting", "Training" etc. The default types (email, chat, ticket, call) are reserved and should not be created over API.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `CustomField`

**Source:** [`types.py:327`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L327)

Most objects in Planaht can be customized by creating your own custom fields. Which model a given custom fields belongs is indicated by the parent property.

Typically you would create the custom fields from within the Planhat app. But in some special cases you may find it more convenient to manage over API instead.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Enduser`

**Source:** [`types.py:343`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L343)

An enduser represents an individual at one of your customers, typically a user of your product, a business contact or both. Endusers can automatically be created based on user tracking events, or based on conversations such as emails and tickets.

Often this automatic creation of contacts along with sync from an external CRM or similar is enough. But there are also situations where you may want to be 100% sure all your users exist in Planhat, and then it would make sense to create them in Planhat over api as soon as they get created in your own system.

If companyId is not present in the payload, and the email has a domain already registered within a company, then Planhat will auto-assign the new enduser to the company using domain matching.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Invoice`

**Source:** [`types.py:361`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L361)

Invoices are normally generated automatically in Planhat when a license is created or renewed, invoices can include multiple line items. Planhat will not prepare invoices that you actually can send to your customers though. They're rather meant to help anyone working with your customers to know the status of current and past invoicing.

Invoices default date fields format should be days format integer. (Days since January 1, 1970, Unix epoch)

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Issue`

**Source:** [`types.py:372`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L372)

Issues typically represent Bugs or Feature Requests. Many of our customers fetch issues from Jira, but they can also be pushed to Planhat from other product management tools such as Product Board or Aha! You can also manage issues directly in Planhat without any external tool. Just keep in mind that the functionality is basic and mostly intended to contribute to the customer 360 view.

Issues in Planhat can link to multiple companies, to multiple endusers and to multiple conversations.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `License`

**Source:** [`types.py:403`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L403)

Licenses represent your customers' subcriptions to your service and is the base for MRR (or ARR) calculations and most revenue reports. For non recurring revenue, please see the Sale (NRR) object. There are many ways to get license data into Planhat including incomming webhooks and CRM integrations. In some case though, you just want to handle it yourself over the api, for example if the main source of license data is your own system.

Licenses in Planhat can be fixed period with a defined start and end date. Or they can be non fixed period (sometimes called open-ended or evergreen). Open ended licenses initially don't have a specified end date since the customer may cancel at any time.. once the license is churned/lost also non fixed period licenses can have an end date.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Note`

**Source:** [`types.py:414`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L414)

Notes in Planhat are technically Conversations. You can create your own custom Touch Types to easily distinguish between different types of notes. You can also use custom fields to add more nuance to your Notes.

It's quite common for Notes in Planhat to sync with external systems such as Salesforce, Notes can also be created via Zapier or Planhats's native incoming webhooks.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `NPS`

**Source:** [`types.py:423`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L423)

NPS records in Planhat represent the individual responses to an nps survey. Typically these are created automatically when running an nps campaign in Planhat, or in some cases imported from external NPS tools. A single enduser/contact can have multiple records if they responded to different surveys over time.

Based on the NPS records each enduser and company in Planhat also get an nps score assigned.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Opportunity`

**Source:** [`types.py:439`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L439)

Opportunities in Planhat represent a sales opportunity, whether it's selling to a new customer or more commonly a chance of expanding an existing account.

Opportunities are not the sames as Licenses, but when an opportunity is closed won in Planhat, there is an optional setting to generate a licenses based on the opportunity data.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Objective`

**Source:** [`types.py:450`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L450)

Being very clear and focused on your goals with customers is critical, and now you can track objectives and the health per objective.

Pro-tip: use your average Objective health in the Health Score!

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Project`

**Source:** [`types.py:461`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L461)

Projects can represent many different real world objects with a natural start and stop date. A service provider for schools may use Projects to represent classes or courses. If you're selling a software to run sales competitions, then each competition may be a project.

Using custom fields you can tailor projects to your needs, and just like Assets, usage data and time series data (metrics) can be associated with your Projetcs.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Sale`

**Source:** [`types.py:472`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L472)

The Sale (NRR) model represents not recurring revenue, like an onboarding fee, or a one-off professional services project.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Task`

**Source:** [`types.py:480`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L480)

Tasks are the things that you plan to do in the future. It can be a simple "to-do" without any specific due date, a reminder of something to be done at a specific point in time, or even a meeting with a start and end time.

Most of the time these tasks will be automatically generated in Planhat based on rules you set up. It's also comon to have tasks as steps in a Playbook. But tasks can also be created ad-hoc just like you would in any task management app.

Tasks managed over the API should typically have the mainType property set to `task`, the other potential value is `event`, which indicates that it was synced to or from a calendar like Google Calendar. Though it's also possible to create tasks of type event in Planhat without syncing them back to any calendar.

Once a task is completed it's archived and genrally not visble in Planhat anymore. Sometimes when completing a tasks, say a training session, you want to log a note summarizing how it went, this is managed automatically by Planhat when working in the Planhat app.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Ticket`

**Source:** [`types.py:500`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L500)

Tickets in Planhat are Conversations, so if you plan to send tickets to Planhat via API then you can also use that endpoint. The ticket endpoint contains a bit of convenience logic for save tickets specificially, like setting the proper type automatically.

Most of our customers sync tickets from an external system like Zendesk or Salesforce. In case your ticketing system isn't natively supported or you have your own system for it, please let us know and we'll be happy to discuss how to best work with this api.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `User`

**Source:** [`types.py:516`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L516)

Users are all your team members that need access to Planhat. Users can be created in the app, using spreadsheet upload or over api. If you're using teams to group your users in Planhat you'll need to call a separate endpoint to associate your Users with the right teams.

If a user is flagged as inactive, they will not be able to login to Planhat and they will not get notifications, but they will be available for assigning accounts etc.

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `Workspace`

**Source:** [`types.py:542`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L542)

If you work with sub-instances at your customers, e.g., connecting with different departments or with different versions of your product (think like a Workspace in Slack), then this is the object to track that engagement!

### method `__init__`

**Source:** [`types.py:133`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L133)

```python
__init__(data: dict | None = None)
```

Initializes the Planhat object using the provided dictionary. If you want to initialize an object from an API response, use the class factory method from_response() instead.

:param data: A dictionary containing the Planhat object.

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

**Source:** [`types.py:233`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L233)

```python
encode() → bytes
```

Encodes the object as a byte-like JSON string for API body payloads

______________________________________________________________________

### classmethod `from_list`

**Source:** [`types.py:122`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L122)

```python
from_list(data: list[dict]) → PlanhatObjectList[O]
```

Creates a PlanhatList from a list of dictionaries.

:param data: A list of dictionaries representing Planhat objects.

______________________________________________________________________

### classmethod `from_response`

**Source:** [`types.py:54`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L54)

```python
from_response(response: Response) → O | PlanhatObjectList[O]
```

Creates a Planhat object or list of Planhat objects from a response from Planhat.

:param response: The response from Planhat.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:197`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L197)

```python
get_urlpath(id_type: PlanhatIdType = <PlanhatIdType.PLANHAT_ID: ''>) → str
```

Returns the URL path for the object utilizing the provided ID type. Falls back to any ID type if the provided ID type is not available.

:param id_type: The ID type to use when generating the URL path.

______________________________________________________________________

### method `is_same_object`

**Source:** [`types.py:185`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L185)

```python
is_same_object(other: object) → bool
```

Returns whether the other object is the same Planhat object. This is determined by comparing the IDs of the objects.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:239`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L239)

```python
to_serializable_json() → dict
```

Return a dictionary where all `datetime` objects within the object are converted to ISO 8601 strings.

______________________________________________________________________

## class `PlanhatObjectList`

**Source:** [`types.py:555`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L555)

A list of Planhat objects.

### method `__init__`

**Source:** [`types.py:558`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L558)

```python
__init__(_PlanhatObjectList__iterable: Optional[Iterable[~O]] = None) → None
```

Initializes the Planhat list using the provided list of Planhat objects. The type of the first object in the list is used to determine the type of the list.

:param data: A list of Planhat objects.

______________________________________________________________________

### method `append`

**Source:** [`types.py:655`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L655)

```python
append(obj: ~O) → None
```

Appends a Planhat object to the list.

______________________________________________________________________

### method `encode`

**Source:** [`types.py:767`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L767)

```python
encode() → bytes
```

Encodes the list as a byte-like JSON string for API body payloads

______________________________________________________________________

### method `extend`

**Source:** [`types.py:671`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L671)

```python
extend(objs: 'PlanhatObjectList[O] | Sequence[O]') → None
```

Extends the list with a list of Planhat objects.

______________________________________________________________________

### method `find_by_company_id`

**Source:** [`types.py:743`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L743)

```python
find_by_company_id(company_id: str) → PlanhatObjectList[O]
```

Returns the Planhat objects with the provided company ID.

______________________________________________________________________

### method `find_by_external_id`

**Source:** [`types.py:730`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L730)

```python
find_by_external_id(external_id: str) → ~O
```

Returns the Planhat objects with the provided external ID.

______________________________________________________________________

### method `find_by_id`

**Source:** [`types.py:704`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L704)

```python
find_by_id(id: str) → ~O
```

Returns the Planhat object with the provided ID.

______________________________________________________________________

### method `find_by_source_id`

**Source:** [`types.py:717`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L717)

```python
find_by_source_id(source_id: str) → ~O
```

Returns the Planhat objects with the provided source ID.

______________________________________________________________________

### method `get_urlpath`

**Source:** [`types.py:780`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L780)

```python
get_urlpath() → str
```

Returns the URL path for object type of the list.

______________________________________________________________________

### method `insert`

**Source:** [`types.py:680`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L680)

```python
insert(index: <class 'SupportsIndex'>, obj: ~O) → None
```

Inserts a Planhat object at the provided index.

______________________________________________________________________

### method `is_obj_in_list`

**Source:** [`types.py:694`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L694)

```python
is_obj_in_list(obj: ~O) → bool
```

Returns whether the provided Planhat object is in the list based on IDs.

______________________________________________________________________

### method `remove`

**Source:** [`types.py:688`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L688)

```python
remove(obj: ~O) → None
```

Removes a Planhat object from the list.

______________________________________________________________________

### method `to_serializable_json`

**Source:** [`types.py:773`](https://github.com/robocorp/robocorp-planhat/tree/master/src/planhat/types.py#L773)

```python
to_serializable_json() → list[dict]
```

Return a list of dictionaries where all `datetime` objects within the objects are converted to ISO 8601 strings.
