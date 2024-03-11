"""Data types used in the Planhat client."""

import datetime
import itertools
import json
import logging
from abc import ABC
from collections import defaultdict
from collections.abc import Iterator
from enum import Enum
from typing import Any, Iterable, Self, Type, TypeVar, overload
from urllib import parse

from requests import Response
from robocorp import log  # Remove once logging is integrated into log
from typing_extensions import SupportsIndex

from .errors import PlanhatNotFoundError

BO = TypeVar("BO", bound="PlanhatBaseObject")
MO = TypeVar("MO", bound="PlanhatObject")


def _all_subclasses(cls: type[BO]) -> set[type[BO]]:
    """Returns all subclasses of the provided class."""
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in _all_subclasses(c)]
    )


def _get_type_name_from_response(response: Response) -> str:
    """
    Extracts the Planhat object type from the request attached to the response.

    Args:
        response: The response from Planhat.

    Returns:
        The type of the Planhat object.

    Raises:
        ValueError: If unable to parse path from URL or find Planhat object
            type for endpoint.
    """
    _, _, path, _, _ = parse.urlsplit(response.request.url)
    # The third component should reference the endpoint for the object
    # type, because the path should look like "/companies" or "/endusers".
    if isinstance(path, str):
        type_name = path.split("/")[1]
    else:
        raise ValueError(f"Unable to parse path from URL {response.request.url}.")
    return type_name


def _get_type(
    type: str, cls: type[BO] = "PlanhatBaseObject"
) -> type["PlanhatBaseObject"]:
    """
    Returns the type of the Planhat object from the provided type string.

    Args:
        type: The type string to parse.

    Returns:
        The type of the Planhat object.
    """
    for subclass in _all_subclasses(cls):
        if (
            (subclass.API_NAME or "").lower() == type.lower()
            or (subclass.PLURAL or "").lower() == type.lower()
            or (subclass.SINGULAR or "").lower() == type.lower()
            or subclass.__name__.lower() == type.lower()
        ):
            return subclass
    raise ValueError(f"Unable to find Planhat object type for endpoint {type}.")


class PlanhatIdType(Enum):
    PLANHAT_ID = ""
    SOURCE_ID = "srcid-"
    EXTERNAL_ID = "extid-"


class DateTimeEncoder(json.JSONEncoder):
    """A custom JSON encoder for use with Planhat objects."""

    def default(self, obj: Any) -> Any:
        """Returns a JSON-serializable version of the provided object."""
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return obj.total_seconds()
        else:
            return super().default(obj)


class PlanhatBaseObject(dict[str, Any], ABC):
    """
    A base Planhat object. This is a dictionary with some additional
    functionality.

    The dictionary is the JSON response from Planhat or a dictionary containing
    the Planhat object.

    The class includes several class methods to facilitate creation of objects
    from API responses or lists of dictionaries. It also includes methods to
    facilitate encoding the object as a JSON string for API requests.

    When creating objects using dictionaries, you must use the keys that
    Planhat uses in its API responses. For example, the key for the Planhat ID
    is "_id". See Planhat API documentation for more information.

    Example usage:

        from planhat import PlanhatObject

        # Create a Planhat object from a dictionary
        data = {
            "_id": "123",
            "name": "Company A"
        }
        company = PlanhatObject(data)

        # Create a Planhat object from an API response
        response = requests.get("https://api.planhat.com/companies/123")
        company = PlanhatObject.from_response(response)

        # Create a Planhat object from a list of dictionaries
        data = [
            {
                "_id": "123",
                "name": "Company A"
            },
            {
                "_id": "456",
                "name": "Company B"
            }
        ]
        companies = PlanhatObject.from_list(data)
    """

    API_NAME: str | None = None
    """The API name for the Planhat object. Used to form the endpoint."""
    SINGULAR: str | None = None
    """The singular form of the Planhat model type."""
    PLURAL: str | None = None
    """The plural form of the Planhat model type."""

    @classmethod
    def from_response(
        cls: type[BO],
        response: Response,
    ) -> "BO | PlanhatBaseObjectList[BO]":
        """
        Creates a Planhat object or list of Planhat objects from a
        response from Planhat.

        Args:
            response: The response from Planhat.

        Returns:
            A Planhat object or list of Planhat objects.

        Raises:
            TypeError: If the response from Planhat is not dictionary- or
                list-like.
        """
        data = response.json()
        if cls is PlanhatBaseObject or cls is PlanhatObject:
            cls = cls._extract_type_from_response(response)
        if isinstance(data, dict):
            return cls._from_single_response(response)
        elif isinstance(data, list):
            objs = cls.from_list(data)
            for obj in objs:
                obj._response = response
            return objs
        else:
            raise TypeError(
                "The response from Planhat is not dictionary- or list-like."
            )

    @classmethod
    def _extract_type_from_response(cls: type[BO], response: Response) -> Type[BO]:
        """
        Extracts the Planhat object type from the request attached to the response.

        Args:
            response: The response from Planhat.

        Returns:
            The type of the Planhat object.

        Raises:
            ValueError: If unable to parse path from URL or find Planhat object
                type for endpoint.
        """
        type_name = _get_type_name_from_response(response)
        # Look through the subclasses and match on API_NAME
        try:
            return _get_type(type_name, cls)
        except ValueError:
            raise ValueError(
                f"Unable to find Planhat object type for endpoint {response.request.url}."
            )

    @classmethod
    def _from_single_response(cls: type[BO], response: Response) -> BO:
        """
        Creates a Planhat object from a response from Planhat.

        Args:
            response: The response from Planhat.

        Returns:
            A Planhat object.

        Raises:
            TypeError: If the response from Planhat is not dictionary-like.
        """
        data = response.json()
        if isinstance(data, dict):
            obj = cls(data)
            obj._response = response
            return obj
        else:
            raise TypeError("The response from Planhat is not dictionary-like.")

    @classmethod
    def from_list(
        cls: type[BO],
        data: list[dict],
    ) -> "PlanhatBaseObjectList[BO]":
        """
        Creates a Planhat list from a list of dictionaries.

        Args:
            data: A list of dictionaries representing Planhat objects. The
                keys must match the Planhat API endpoint keys.
        """
        return PlanhatBaseObjectList(cls(item) for item in data)

    @classmethod
    def get_type_urlpath(self) -> str:
        """Returns the URL path for the the object type."""
        return f"/{self.API_NAME}"

    def __init__(
        self,
        data: dict | None = None,
        id: str | None = None,
    ):
        """
        Initializes the Planhat object using the provided dictionary or ID.

        You may initialize the object with a dictionary containing the object
        data, or by providing the ID. If you provide a dictionary, all other
        parameters are ignored.

        If you want to initialize an object from an API response, use the
        class factory method from_response() instead.

        Args:
            data: A dictionary containing the Planhat object. If provided,
                all other parameters are ignored.
            id: The Planhat ID of the object.
        """
        self._response: Response | None = None
        if data is not None:
            super().__init__(data)
        elif id:
            init_data: dict[str, Any] = {}
            if id is not None:
                init_data["_id"] = id
            super().__init__(init_data)
        else:
            super().__init__()

    def __repr__(self) -> str:
        """Returns a string representation of the Planhat object."""
        return f"{self.__class__.__name__}" f"(id={self.id})"

    def __str__(self) -> str:
        """Returns a string representation of the Planhat object."""
        return self.__repr__()

    @property
    def response(self) -> Response | None:
        """Returns the response from Planhat which originated this object."""
        return self._response

    @property
    def id(self) -> str:
        """Returns the Planhat ID of the object."""
        return self.get("_id", "")

    @id.setter
    def id(self, value: str) -> None:
        self["_id"] = value

    def is_same_object(self, other: object) -> bool:
        """
        Returns whether the other object is the same Planhat object by
        by comparing the IDs of the objects.
        """
        if not isinstance(other, PlanhatObject):
            return False
        if self.id and other.id and self.id == other.id:
            return True

        return False

    def get_base_urlpath(self) -> str:
        """
        Returns the URL path for the object type.
        """
        return f"/{self.API_NAME}"

    def _dump(self) -> str:
        """Returns the object as a JSON string."""
        return json.dumps(self, cls=DateTimeEncoder, allow_nan=False)

    def encode(self) -> bytes:
        """
        Encodes and returns  the object as a byte-like JSON string for API
        body payloads.
        """
        return bytes(self._dump(), encoding="utf-8")

    def to_serializable_json(self) -> dict:
        """
        Returns a dictionary where all `datetime` objects within the object
        are converted to ISO 8601 strings.
        """
        return json.loads(self._dump())


class PlanhatObject(PlanhatBaseObject, ABC):
    """
    A Planhat model object.

    This class and it's subclasses are used to represent the different types of
    data models in the Planhat system and REST API.
    """

    @classmethod
    def from_list(cls: type[MO], data: list[dict]) -> "PlanhatObjectList[MO]":
        return PlanhatObjectList(cls(item) for item in data)

    def __init__(
        self,
        *args,
        source_id: str | None = None,
        external_id: str | None = None,
        custom: dict | None = None,
        **kwargs,
    ):
        """
        Initializes the Planhat object.

        You may initialize the object with a dictionary containing the object
        data, or by providing the ID, source ID, external ID, and/or custom fields.
        If you provide a dictionary, all other parameters are ignored.

        Args:
            data: A dictionary containing the Planhat object. If provided,
                all other parameters are ignored.
            id: The Planhat ID of the object.
            source_id: The source ID of the object.
            external_id: The external ID of the object.
            custom: The custom fields of the object.
        """
        super().__init__(*args, **kwargs)
        if source_id is not None:
            self.source_id = source_id
        if external_id is not None:
            self.external_id = external_id
        if custom is not None:
            self.custom = custom

    def __repr__(self) -> str:
        """Returns a string representation of the Planhat object."""
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, source_id={self.source_id}, external_id={self.external_id})"
        )

    @property
    def external_id(self) -> str:
        """Returns the external ID of the object."""
        return self.get("externalId", "")

    @external_id.setter
    def external_id(self, value: str) -> None:
        self["externalId"] = value

    @property
    def source_id(self) -> str:
        """Returns the source ID of the object."""
        return self.get("sourceId", "")

    @source_id.setter
    def source_id(self, value: str) -> None:
        self["sourceId"] = value

    @property
    def custom(self) -> dict:
        """Returns the custom fields of the object."""
        return self.get("custom", {})

    @custom.setter
    def custom(self, value: dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("Custom fields must be a dictionary.")
        self["custom"] = value

    def is_same_object(self, other: object) -> bool:
        """
        Returns whether the other object is the same Planhat object by
        by comparing the IDs of the objects.
        """
        if not isinstance(other, PlanhatObject):
            return False
        if self.id and other.id and self.id == other.id:
            return True
        if self.source_id and other.source_id and self.source_id == other.source_id:
            return True
        if (
            self.external_id
            and other.external_id
            and self.external_id == other.external_id
        ):
            return True

        return False

    def get_urlpath(self, id_type: PlanhatIdType = PlanhatIdType.PLANHAT_ID) -> str:
        """
        Returns the URL path for the object utilizing the provided ID type.
        Falls back to any ID type if the provided ID type is not available.

        Args:
            id_type: The ID type to use when generating the URL path.

        Returns:
            The URL path for the object.
        """
        if id_type == PlanhatIdType.PLANHAT_ID and self.id:
            return f"{self.get_base_urlpath()}/{self.id}"
        elif id_type == PlanhatIdType.SOURCE_ID and self.source_id:
            return f"{self.get_base_urlpath()}/{id_type.value}{self.source_id}"
        elif id_type == PlanhatIdType.EXTERNAL_ID and self.external_id:
            return f"{self.get_base_urlpath()}/{id_type.value}{self.external_id}"
        else:
            return self._get_any_urlpath()

    def _get_any_urlpath(self) -> str:
        """
        Returns the URL path for the object utilizing any ID type.
        Always returns an ID based on the following priority:

        1. Planhat ID
        2. Source ID
        3. External ID

        Returns:
            str: The URL path for the object.
        """
        if self.id:
            return self.get_urlpath(PlanhatIdType.PLANHAT_ID)
        elif self.source_id:
            return self.get_urlpath(PlanhatIdType.SOURCE_ID)
        elif self.external_id:
            return self.get_urlpath(PlanhatIdType.EXTERNAL_ID)
        else:
            raise ValueError("Unable to determine ID for object.")


class NamedObjectMixin(PlanhatObject, ABC):
    def __init__(self, *args, name: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if name is not None:
            self.name = name

    @property
    def name(self) -> str:
        """The name of the object."""
        return self.get("name", "")

    @name.setter
    def name(self, value: str) -> None:
        self["name"] = value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name={self.name}, id={self.id}, source_id={self.source_id}, external_id={self.external_id})"
        )


class Company(NamedObjectMixin, PlanhatObject):
    """
    Class to represent Companies ("accounts"), which are your customers.

    Depending on your business these might be agencies, schools, other businesses or something else.
    Companies can also be your previous customers and potentially future customers (prospects).

    The company object is one of the most central in Planhat since most other objects relate to it,
    and it's frequently used to filter out other information, such as endsuers, licenses, notes etc.

    In Planhat it is possible have a hierarchical structure for the companies,
    meaning that they can be grouped into organizations with parents and children in a tree like structure.
    """

    API_NAME = "companies"
    SINGULAR = "company"
    PLURAL = "companies"


class PlanhatCompanyOwnedObject(PlanhatObject, ABC):
    """An abstract class representing objects that are owned by a company."""

    def __init__(
        self,
        *args,
        company_id: str | None = None,
        company_name: str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if company_id is not None:
            self.company_id = company_id
        if company_name is not None:
            self.company_name = company_name

    @property
    def company_id(self) -> str:
        """The ID of the company that owns this object."""
        return self.get("companyId", self.get("cId", ""))

    @company_id.setter
    def company_id(self, value: str) -> None:
        self["companyId"] = value

    @property
    def company_name(self) -> str:
        """The name of the company that owns this object."""
        return self.get("companyName", self.get("cName", ""))

    @company_name.setter
    def company_name(self, value: str) -> None:
        self["companyName"] = value


class Asset(PlanhatCompanyOwnedObject):
    """
    Assets in Planhat can represent many different things depending on your use case.
    It could be drones, if you're selling a drone tracking product, or it could be instances
    of your product in cases where a single customer can run multiple instances of your product
    in parallel. Assets could also represent your different products.

    More generally, Assets are "nested objects" for which you may want to track usage separately,
    but don't need to treat them as separate customers with individual contacts, conversations, etc.
    """

    API_NAME = "assets"
    SINGULAR = "asset"
    PLURAL = "assets"


class Campaign(PlanhatCompanyOwnedObject):
    """
    Manage campaigns you are running inside companies, e.g., to drive adoption
    or to deepen stakeholder relations.
    """

    API_NAME = "campaigns"
    SINGULAR = "campaign"
    PLURAL = "campaigns"


class Churn(PlanhatCompanyOwnedObject):
    """
    Each time one of your customers churns or downgrades you can add a specific
    log about this. Mostly this "churn log" is added manually by the CSM from
    within Planhat, but there may also be times when you want to add it over
    API, for example if you're capturing information about downgrades and
    churn natively in-app in your own platform and want to send that over
    to Planhat.

    The churn logs in Planhat typically contain the reasons for the churn,
    the value, date etc. It's important to note though that it doesn't affect
    actual revenue numbers and KPIs such as churn rate, renewal rate etc, on
    it's own. Those calculations are entirely based on underlying license data.
    """

    API_NAME = "churn"
    SINGULAR = "churn"
    PLURAL = "churns"


class Conversation(PlanhatCompanyOwnedObject):
    """
    Represents conversations of different types.

    This class represents conversations of various types such as email, chat,
    support tickets, and manually logged notes. Custom types can also be
    created in Planhat to represent things such as "in person meeting",
    "Training" etc. The default types (email, chat, ticket, call) are
    reserved and should not be created over API.
    """

    API_NAME = "conversations"
    SINGULAR = "conversation"
    PLURAL = "conversations"


class CustomField(PlanhatObject):
    """
    Represents custom fields in Planhat.

    Most objects in Planhat can be customized by creating your own custom
    fields. The parent property indicates which model a given custom field
    belongs to. Typically, custom fields are created from within the Planhat
    app. However, in some special cases, managing over API may be more
    convenient.
    """

    API_NAME = "customfields"
    SINGULAR = "custom field"
    PLURAL = "custom fields"

    def __init__(self, *args, parent: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if parent is not None:
            self.parent = parent

    @property
    def parent(self) -> str:
        """The singular name of the parent model which owns this custom field"""
        return self.get("parent", "")

    @parent.setter
    def parent(self, value: str) -> None:
        self["parent"] = value


class Enduser(PlanhatCompanyOwnedObject):
    """
    Represents an individual at one of your customers. This could be a user of
    your product, a business contact or both. Endusers can be created
    automatically based on user tracking events, or based on conversations such
    as emails and tickets.

    Often, automatic creation of contacts along with sync from an external CRM
    or similar is enough. But there are also situations where you may want to
    be 100% sure all your users exist in Planhat, and then it would make sense
    to create them in Planhat over API as soon as they get created in your own
    system.

    If 'companyId' is not present in the payload, and the email has a domain
    already registered within a company, then Planhat will auto-assign the new
    enduser to the company using domain matching.
    """

    API_NAME = "endusers"
    SINGULAR = "enduser"
    PLURAL = "endusers"

    def __init__(self, *args, email: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if email is not None:
            self.email = email

    @property
    def email(self) -> str:
        """The email address of the enduser."""
        return self.get("email", "")

    @email.setter
    def email(self, value: str) -> None:
        self["email"] = value


class Invoice(PlanhatCompanyOwnedObject):
    """
    Represents Invoices in Planhat.

    Invoices are normally generated automatically in Planhat when a license is
    created or renewed. Each invoice can include multiple line items. However,
    Planhat does not prepare invoices that can be sent to customers. They are
    primarily meant to help anyone working with your customers to know the
    status of current and past invoicing.

    Note:
        The default date fields format for invoices should be in integer days
        format (Days since January 1, 1970, Unix epoch).
    """

    API_NAME = "invoices"
    SINGULAR = "invoice"
    PLURAL = "invoices"


class Issue(PlanhatObject):
    """
    Issues typically represent Bugs or Feature Requests. Many of our customers
    fetch issues from Jira, but they can also be pushed to Planhat from other
    product management tools such as Product Board or Aha! You can also manage
    issues directly in Planhat without any external tool. Just keep in mind that
    the functionality is basic and mostly intended to contribute to the customer
    360 view.

    Issues in Planhat can link to multiple companies, to multiple endusers and
    to multiple conversations.
    """

    API_NAME = "issues"
    SINGULAR = "issue"
    PLURAL = "issues"

    def __init__(
        self,
        *args,
        company_ids: list[str] | None = None,
        company_names: list[str] | None = None,
        enduser_ids: list[str] | None = None,
        enduser_names: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if company_ids is not None:
            self.company_ids = company_ids
        if company_names is not None:
            self.company_names = company_names
        if enduser_ids is not None:
            self.enduser_ids = enduser_ids
        if enduser_names is not None:
            self.enduser_names = enduser_names

    @property
    def company_ids(self) -> list[str]:
        """The IDs of the companies that this issue is linked to."""
        return self.get("companyIds", [])

    @company_ids.setter
    def company_ids(self, value: list[str]) -> None:
        self["companyIds"] = value

    @property
    def company_names(self) -> list[str]:
        """The names of the companies that this issue is linked to."""
        return self.get("companies", [])

    @company_names.setter
    def company_names(self, value: list[str]) -> None:
        self["companies"] = value

    @property
    def enduser_ids(self) -> list[str]:
        """The IDs of the endusers that this issue is linked to."""
        return self.get("enduserIds", [])

    @enduser_ids.setter
    def enduser_ids(self, value: list[str]) -> None:
        self["enduserIds"] = value

    @property
    def enduser_names(self) -> list[str]:
        """The names of the endusers that this issue is linked to."""
        return self.get("endusers", [])

    @enduser_names.setter
    def enduser_names(self, value: list[str]) -> None:
        self["endusers"] = value


class License(PlanhatCompanyOwnedObject):
    """
    Represents your customers' subscriptions to your service. This is the base
    for MRR (or ARR) calculations and most revenue reports. For non-recurring
    revenue, refer to the Sale (NRR) object. There are many ways to get license
    data into Planhat including incoming webhooks and CRM integrations. In some
    cases, handling it over the API is preferred, for example if the main source
    of license data is your own system.

    Licenses in Planhat can be fixed period with a defined start and end date, or
    they can be non-fixed period (sometimes called open-ended or evergreen).
    Open-ended licenses initially don't have a specified end date since the
    customer may cancel at any time. Once the license is churned/lost, non-fixed
    period licenses can also have an end date.
    """

    API_NAME = "licenses"
    SINGULAR = "license"
    PLURAL = "licenses"


class Note(Conversation):
    """
    Notes in Planhat are technically Conversations. You can create your own
    custom Touch Types to easily distinguish between different types of notes.
    You can also use custom fields to add more nuance to your Notes.

    It's quite common for Notes in Planhat to sync with external systems such as
    Salesforce, Notes can also be created via Zapier or Planhats's native
    incoming webhooks.
    """

    pass


class NPS(PlanhatCompanyOwnedObject):
    """
    Represents the individual responses to an NPS survey in Planhat. These are
    typically created automatically when running an NPS campaign in Planhat, or
    sometimes imported from external NPS tools. A single enduser/contact can
    have multiple records if they responded to different surveys over time.

    Based on the NPS records, each enduser and company in Planhat also get an
    NPS score assigned.
    """

    API_NAME = "nps"
    SINGULAR = "nps"
    PLURAL = "nps"

    def __init__(self, *args, campaign_id: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if campaign_id is not None:
            self.campaign_id = campaign_id

    @property
    def campaign_id(self) -> str:
        """The ID of the campaign that this NPS record is linked to."""
        return self.get("campaignId", "")

    @campaign_id.setter
    def campaign_id(self, value: str) -> None:
        self["campaignId"] = value


class Opportunity(PlanhatCompanyOwnedObject):
    """
    Represents a sales opportunity in Planhat. This could be a chance to sell to
    a new customer or more commonly, an opportunity to expand an existing account.

    Note:
        Opportunities are not the same as Licenses. However, when an opportunity
        is closed won in Planhat, there is an optional setting to generate a
        license based on the opportunity data.
    """

    API_NAME = "opportunities"
    SINGULAR = "opportunity"
    PLURAL = "opportunities"


class Objective(PlanhatCompanyOwnedObject):
    """
    Represents the objectives and their health in Planhat.

    This class is critical for tracking objectives and the health per objective.

    Pro-tip: use your average Objective health in the Health Score!
    """

    API_NAME = "objectives"
    SINGULAR = "objective"
    PLURAL = "objectives"


class Project(PlanhatCompanyOwnedObject):
    """
    Represents Projects in Planhat.

    Projects can represent many different real world objects with a natural start
    and stop date. For example, a service provider for schools may use Projects
    to represent classes or courses. If you're selling a software to run sales
    competitions, then each competition may be a project.

    Using custom fields, projects can be tailored to specific needs. Just like
    Assets, usage data and time series data (metrics) can be associated with
    your Projects.
    """

    API_NAME = "projects"
    SINGULAR = "project"
    PLURAL = "projects"


class Sale(PlanhatCompanyOwnedObject):
    """
    The Sale (NRR) model represents not recurring revenue, like an onboarding
    fee, or a one-off professional services project.
    """

    API_NAME = "sales"
    SINGULAR = "sale"
    PLURAL = "sales"


class Task(PlanhatCompanyOwnedObject):
    """
    Represents tasks in Planhat. Tasks are future actions, which can be simple
    "to-do" items without a specific due date, reminders for a specific time,
    or meetings with a start and end time.

    Most tasks are automatically generated in Planhat based on set rules. They
    can also be steps in a Playbook or created ad-hoc like in any task
    management app.

    Tasks managed over the API should typically have the mainType property set
    to `task`. Another potential value is `event`, indicating a sync to or from
    a calendar like Google Calendar. Tasks of type `event` can also be created in
    Planhat without syncing them back to any calendar.

    Once a task is completed, it's archived and generally not visible in
    Planhat anymore. Sometimes, when completing a task like a training session,
    a note summarizing how it went is logged. This is managed automatically by
    Planhat when working in the Planhat app.
    """

    API_NAME = "tasks"
    SINGULAR = "task"
    PLURAL = "tasks"

    def __init__(self, *args, task_type: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if task_type is not None:
            self.task_type = task_type

    @property
    def task_type(self) -> str:
        """The type of task that this task is."""
        return self.get("type", "")

    @task_type.setter
    def task_type(self, value: str) -> None:
        self["type"] = value


class Ticket(PlanhatCompanyOwnedObject):
    """
    Tickets in Planhat are Conversations. If you plan to send tickets to Planhat
    via API, you can also use that endpoint. The ticket endpoint contains
    convenience logic for saving tickets specifically, like setting the proper
    type automatically.

    Most customers sync tickets from an external system like Zendesk or
    Salesforce. If your ticketing system isn't natively supported or you have
    your own system, please let us know. We'll be happy to discuss how to best
    work with this API.
    """

    API_NAME = "tickets"
    SINGULAR = "ticket"
    PLURAL = "tickets"

    def __init__(self, *args, email: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if email is not None:
            self.email = email

    @property
    def email(self) -> str:
        """The email address of user who submitted the ticket."""
        return self.get("email", "")

    @email.setter
    def email(self, value: str) -> None:
        self["email"] = value


class User(PlanhatObject):
    """
    Represents a User in Planhat.

    Users are all your team members that need access to Planhat. Users can be
    created in the app, using spreadsheet upload or over API. If you're using
    teams to group your users in Planhat you'll need to call a separate endpoint
    to associate your Users with the right teams.

    If a user is flagged as inactive, they will not be able to login to Planhat
    and they will not get notifications, but they will be available for
    assigning accounts etc.
    """

    API_NAME = "users"
    SINGULAR = "user"
    PLURAL = "users"

    def __init__(
        self,
        *args,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if email is not None:
            self.email = email
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name

    @property
    def email(self) -> str:
        """The email address of the user."""
        return self.get("email", "")

    @email.setter
    def email(self, value: str) -> None:
        self["email"] = value

    @property
    def first_name(self) -> str:
        """The first name of the user."""
        return self.get("firstName", "")

    @first_name.setter
    def first_name(self, value: str) -> None:
        self["firstName"] = value

    @property
    def last_name(self) -> str:
        """The last name of the user."""
        return self.get("lastName", "")

    @last_name.setter
    def last_name(self, value: str) -> None:
        self["lastName"] = value


class Workspace(PlanhatCompanyOwnedObject):
    """
    If you work with sub-instances at your customers, e.g., connecting
    with different departments or with different versions of your product
    (think like a Workspace in Slack), then this is the object to track
    that engagement!
    """

    API_NAME = "workspaces"
    SINGULAR = "workspace"
    PLURAL = "workspaces"

    def __init__(self, *args, name: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if name is not None:
            self.name = name

    @property
    def name(self) -> str:
        """The name of the workspace."""
        return self.get("name", "")

    @name.setter
    def name(self, value: str) -> None:
        self["name"] = value


class PlanhatBaseObjectList(list[BO]):
    """A list of Planhat objects."""

    def __init__(self, __iterable: Iterable[BO] | None = None) -> None:
        """
        Initializes the Planhat list using the provided list of Planhat
        objects. The type of the first object in the list is used to
        determine the type of the list.

        Args:
            __iterable: A list of Planhat objects.
        """
        if __iterable is None:
            __iterable = []
        super().__init__(__iterable)
        self._type = PlanhatBaseObject
        if len(self) > 0:
            self._set_type_if_not_set(self)
        self._validate()
        self._id_dict: dict[str, BO] = {}
        self.logger = logging.getLogger(__name__)

    def _set_type_if_not_set(self, obj: BO | Iterable[BO]) -> BO | Iterable[BO]:
        """
        Sets the type of the list if it has not been set yet. Returns the
        object or iterable.
        """
        if self._type.API_NAME is not None:
            return obj
        else:
            if isinstance(obj, PlanhatBaseObject):
                self._type = type(obj)
                return obj
            elif isinstance(obj, PlanhatBaseObjectList) and len(obj) > 0:
                if obj._type.API_NAME is not None:
                    self._type = obj._type
                else:
                    self._type = type(obj[0])
                return obj
            elif isinstance(obj, Iterable):
                peeker, iterable = itertools.tee(obj)
                first_item = next(peeker, None)
                if first_item:
                    self._type = type(first_item)
                return iterable

    def _validate(self) -> None:
        """
        Validates the list of Planhat objects by ensuring that all objects
        are of the same type.

        Raises:
            TypeError: If the list contains objects of different types.
        """
        for index, obj in enumerate(self):
            if not isinstance(obj, self._type):
                raise TypeError(
                    f"Expected {self._type.__name__}, got {type(obj).__name__} "
                    f"instead at index {index}."
                )

    @overload
    def __getitem__(self, key: SupportsIndex) -> BO:
        """
        Retrieve the value associated with the given key.

        Parameters:
            key: The key to retrieve the value for.

        Returns:
            The value associated with the given key.

        Raises:
            KeyError: If the key is not found in the collection.
        """
        ...

    @overload
    def __getitem__(self, key: slice) -> "PlanhatObjectList[BO]":
        """
        Retrieve a slice of the PlanhatObjectList.

        Args:
            key: The slice object representing the range of indices to retrieve.

        Returns:
            A new PlanhatObjectList containing the sliced elements.
        """

    def __getitem__(self, key: SupportsIndex | slice) -> "BO | PlanhatObjectList[BO]":
        """
        Returns a Planhat object or a slice of the PlanhatObjectList.

        This method overrides the built-in __getitem__ method to support
        retrieving a single Planhat object by its index or a slice of
        Planhat objects by a range of indices.

        Args:
            key: The index or slice to retrieve the Planhat object(s) from the list.

        Returns:
            If the key is an index, returns a single Planhat object. If the
            key is a slice, returns a new PlanhatObjectList containing the
            sliced elements.

        Raises:
            IndexError: If the key is an index that is out of range.
            TypeError: If the key is not an integer or a slice.
        """
        if isinstance(key, slice):
            return PlanhatObjectList(super().__getitem__(key))
        else:
            return super().__getitem__(key)

    @overload
    def __setitem__(self, key: SupportsIndex, value: BO, /) -> None:
        """
        Set the value of an item in the list.

        Parameters:
            key: The key/index of the item to be set.
            value: The value to be assigned to the item.
        """
        ...

    @overload
    def __setitem__(self, key: slice, value: Iterable[BO], /) -> None:
        """
        Set the value of the specified slice of the PlanhatObjectList.

        Args:
            key: The slice specifying the range of elements to set.
            value: The list of objects to set.
        """
        ...

    def __setitem__(
        self,
        key,
        value,
        /,
    ) -> None:
        iter = self._set_type_if_not_set(value)
        super().__setitem__(key, iter)
        self._validate()

    def __iter__(self) -> Iterator[BO]:
        return super().__iter__()

    def __str__(self) -> str:
        """Returns a string representation of the PlanhatObjectList."""
        return f"{self.__class__.__name__}({super().__str__()})"

    def __repr__(self) -> str:
        """Returns a string representation of the PlanhatObjectList."""
        return f"{self.__class__.__name__}({super().__repr__()})"

    def append(self, obj: BO) -> None:
        """Appends a Planhat object to the list."""
        self._set_type_if_not_set(obj)
        if not isinstance(obj, self._type):
            raise TypeError(f"Expected {self._type}, got {type(obj).__name__} instead.")
        super().append(obj)

    def extend(self, objs: Iterable[BO]) -> None:
        """Extends the list with a list of Planhat objects."""
        iter = self._set_type_if_not_set(objs)
        super().extend(iter)
        self._validate()

    def insert(self, index: SupportsIndex, obj: BO) -> None:
        """Inserts a Planhat object at the provided index."""
        if not isinstance(obj, PlanhatObject):
            raise TypeError(
                f"Expected PlanhatObject, got {type(obj).__name__} instead."
            )
        super().insert(index, obj)

    def remove(self, obj: BO) -> None:
        """
        Removes the first occurance of the provided Planhat object from the list.

        Args:
            obj: The Planhat object to remove from the list.

        Raises:
            TypeError: If the provided object is not of the expected type.
            ValueError: If the provided object is not in the list.
        """
        if not isinstance(obj, self._type):
            raise TypeError(f"Expected {self._type}, got {type(obj).__name__} instead.")
        super().remove(obj)

    def is_obj_in_list(self, obj: BO) -> bool:
        """
        Checks if the provided Planhat object is in the list based on IDs.

        Args:
            obj: The Planhat object to check.

        Returns:
            True if the object is in the list, False otherwise.

        Raises:
            TypeError: If the provided object is not of the expected type.
        """
        if not isinstance(obj, self._type):
            raise TypeError(f"Expected {self._type}, got {type(obj).__name__} instead.")
        for item in self:
            if item.is_same_object(obj):
                return True
        return False

    def find_by_id(self, id: str) -> BO:
        """
        Retrieves the Planhat object using the provided ID.

        Args:
            id: The ID of the Planhat object to retrieve.

        Returns:
            The Planhat object with the provided ID.

        Raises:
            PlanhatNotFoundError: If no Planhat object with the provided ID is found.
        """
        if len(self) != len(self._id_dict):
            self._id_dict = {}
        if not self._id_dict:
            self._id_dict = {obj.id: obj for obj in self}
        try:
            return self._id_dict[id]
        except KeyError:
            raise PlanhatNotFoundError(
                f"Unable to find {self._type.__name__} with ID {id}."
            )

    def _dump(self) -> str:
        """Dumps the list as a JSON string."""
        return json.dumps(self, cls=DateTimeEncoder, allow_nan=False)

    def encode(self) -> bytes:
        """Encodes the list as a byte-like JSON string for API body
        payloads
        """
        return bytes(self._dump(), encoding="utf-8")

    def to_serializable_json(self) -> list[dict]:
        """Return a list of dictionaries where all `datetime` objects within
        the objects are converted to ISO 8601 strings.
        """
        # This is a neat trick from the AI, but will it really work?
        return json.loads(self._dump())

    def get_urlpath(self) -> str:
        """Returns the URL path for object type of the list."""
        if self._type.API_NAME is not None:
            return f"/{self._type.API_NAME}"
        else:
            raise ValueError("Unable to determine URL path for list with no set type.")


class PlanhatListCompanyOwnedMixin(PlanhatBaseObjectList[MO]):
    """A mixin for Planhat lists of company-owned objects."""

    def __init__(self, __iterable: Iterable[MO] | None = None) -> None:
        """
        Initializes the Planhat list using the provided list of Planhat
        objects. The type of the first object in the list is used to
        determine the type of the list.

        Args:
            __iterable: A list of Planhat objects.
        """
        super().__init__(__iterable)
        self._company_id_dict: defaultdict[str, PlanhatBaseObjectList] = defaultdict(
            lambda: PlanhatBaseObjectList()
        )
        self._company_id_dict_value_len = 0

    def find_by_company_id(self, company_id: str) -> "PlanhatBaseObjectList[MO]":
        """
        Returns the Planhat objects associated with the provided company ID.

        Args:
            company_id: The ID of the company.

        Returns:
            A list of Planhat objects associated with the given company ID.
        """
        if len(self) == 0:
            raise ValueError(
                f"Cannot find {self._type.__name__} by company ID because the list is empty."
            )
        type_error_msg = (
            f"Cannot find {self._type.__name__} by company ID because it "
            f"is not a company-owned object."
        )
        if not issubclass(self._type, PlanhatCompanyOwnedObject):
            raise TypeError(type_error_msg)
        if len(self) != self._company_id_dict_value_len:
            self._company_id_dict = defaultdict(lambda: PlanhatBaseObjectList())
            self._company_id_dict_value_len = 0
        if len(self._company_id_dict) == 0:
            for item in self:
                if isinstance(item, self._type):
                    self._company_id_dict[item.company_id].append(item)
                    self._company_id_dict_value_len += 1
                else:
                    raise TypeError(type_error_msg)
            msg = f"Company ID dict: {self._company_id_dict}"
            self.logger.debug(msg)
            log.debug(msg)
        return self._company_id_dict[company_id]


class PlanhatObjectList(PlanhatListCompanyOwnedMixin[MO], PlanhatBaseObjectList[MO]):
    """A list of Planhat objects."""

    def __init__(self, __iterable: Iterable[MO] | None = None) -> None:
        """
        Initializes the Planhat list using the provided list of Planhat
        objects. The type of the first object in the list is used to
        determine the type of the list.

        Args:
            __iterable: A list of Planhat objects.
        """
        super().__init__(__iterable)
        self._source_id_dict: dict[str, MO] = {}
        self._external_id_dict: dict[str, MO] = {}

    def find_by_source_id(self, source_id: str) -> MO:
        """
        Returns the Planhat objects with the provided source ID.

        Args:
            source_id: The source ID of the Planhat object to retrieve.

        Returns:
            The Planhat object with the provided source ID.

        Raises:
            PlanhatNotFoundError: If no Planhat object with the provided source
                ID is found.
        """
        if len(self) != len(self._source_id_dict):
            self._source_id_dict = {}
        if not self._source_id_dict:
            self._source_id_dict = {obj.source_id: obj for obj in self}
        try:
            return self._source_id_dict[source_id]
        except KeyError:
            raise PlanhatNotFoundError(
                f"Unable to find {self._type.__name__} with source ID {source_id}."
            )

    def find_by_external_id(self, external_id: str) -> MO:
        """
        Retrieves the Planhat objects using the provided external ID.

        Args:
            external_id: The external ID of the Planhat object to retrieve.

        Returns:
            The Planhat object with the provided external ID.

        Raises:
            PlanhatNotFoundError: If no Planhat object with the provided
                external ID is found.
        """
        if len(self) != len(self._external_id_dict):
            self._external_id_dict = {}
        if not self._external_id_dict:
            self._external_id_dict = {obj.external_id: obj for obj in self}
        try:
            return self._external_id_dict[external_id]
        except KeyError:
            raise PlanhatNotFoundError(
                f"Unable to find {self._type.__name__} with external ID {external_id}."
            )

    def find_by_id_type(self, id: str, id_type: PlanhatIdType | None = None) -> MO:
        """
        Returns the Planhat object based on the provided ID and ID type.

        Args:
            id: The ID of the Planhat object to retrieve.
            id_type: The type of the ID. If None, defaults to PlanhatIdType.PLANHAT_ID.

        Returns:
            The Planhat object with the provided ID.

        Raises:
            ValueError: If an invalid ID type is provided.
            PlanhatNotFoundError: If no Planhat object with the provided ID is found.
        """
        if id_type is None or id_type == PlanhatIdType.PLANHAT_ID:
            return self.find_by_id(id)
        elif id_type == PlanhatIdType.SOURCE_ID:
            return self.find_by_source_id(id)
        elif id_type == PlanhatIdType.EXTERNAL_ID:
            return self.find_by_external_id(id)
        else:
            raise ValueError(f"Invalid ID type: {id_type}.")


class Metric(PlanhatBaseObject):
    """
    Represents a metric in Planhat.

    Metrics are time series data points that are associated with a specific
    object, such as a company, enduser, asset, or project. They are used to
    track usage, health, or other KPIs over time. Metrics are typically
    created automatically based on user tracking events, but can also be
    created manually or via API.

    Properties of this object represent both an metric to be uploaded and
    a metric retrieved from Planhat. Those properties marked as "cannot be set"
    are only available when the metric is retrieved from Planhat.
    """

    API_NAME = "dimensiondata"
    SINGULAR = "metric"
    PLURAL = "metrics"

    @classmethod
    def from_list(cls, data: list[dict]) -> "MetricList":
        return MetricList(cls(item) for item in data)

    def __init__(
        self,
        *args,
        dimension_id: str | None = None,
        value: int | float = None,
        model_obj: Company | Enduser | Asset | Project | None = None,
        date: datetime.date | None = None,
        **kwargs,
    ):
        """
        Initializes the metric object.

        Args:
            data: A dictionary containing the Planhat object. If provided,
                all other parameters are ignored.
            dimension_id: The ID of the dimension that this metric is associated with.
            value: The value of the metric.
            model_obj: The model object the metric relates to. If you are uploading
                metrics to Planhat, the object must at least have an external
                ID. The object will be populate the external ID and model
                fields for the API.
            date: The date of the metric.
        """
        super().__init__(*args, **kwargs)
        if dimension_id is not None:
            self.dimension_id = dimension_id
        if value is not None:
            self.value = value
        self._model_obj = None
        if model_obj is not None:
            self._model_obj = model_obj
        if date is not None:
            self.date = date

    @property
    def dimension_id(self) -> str:
        """The ID of the dimension that this metric is associated with."""
        return self.get("dimensionId", "")

    @dimension_id.setter
    def dimension_id(self, value: str) -> None:
        self["dimensionId"] = value

    @property
    def value(self) -> int | float:
        """The value of the metric."""
        return self.get("value", 0)

    @value.setter
    def value(self, value: int | float) -> None:
        self["value"] = value

    @property
    def model_obj(self) -> Company | Enduser | Asset | Project:
        """The model object the metric relates to. Defaults to a new Company object."""
        if self._model_obj is None:
            external_id = self.get("externalId", None)
            type_name = self.get("model", None)
            if type_name:
                planhat_type = _get_type(type_name)
                self._model_obj = planhat_type(external_id=external_id)
            self._model_obj = Company(external_id=external_id)
        return self._model_obj

    @model_obj.setter
    def model_obj(self, value: Company | Enduser | Asset | Project) -> None:
        self._model_obj = value

    @property
    def model(self) -> str:
        """The model of the object the metric relates to as a string. Defaults to
        Company. Cannot be set."""
        try:
            return self["model"]
        except KeyError:
            try:
                return self._model_obj.SINGULAR.capitalize()
            except AttributeError:
                return "Company"

    @property
    def external_id(self) -> str:
        """The external ID of the object the metric relates to. Cannot be set."""
        try:
            return self["externalId"]
        except KeyError:
            try:
                return self._model_obj.external_id
            except AttributeError:
                return ""

    @property
    def date(self) -> datetime.date:
        """The date of the metric. Defaults to today's date."""
        internal_date = self.get("date", None)
        if internal_date is not None:
            return datetime.datetime.fromisoformat(internal_date).date()
        return datetime.date.today()

    @date.setter
    def date(self, value: datetime.date) -> None:
        self["date"] = value

    @property
    def day(self) -> int:
        """The number of days since the Unix Epoch. Cannot be set."""
        return self.get("day", int(self.time.timestamp() / 86400))

    @property
    def company_id(self) -> str:
        """
        The ID of the company that this metric is associated with in Planhat.
        Cannot be set.
        """
        return self.get("companyId", "")

    @company_id.setter
    def company_id(self, value: str) -> None:
        self["companyId"] = value

    @property
    def time(self) -> datetime.datetime:
        """The date and time of the metric. Defaults to the current date and time."""
        internal_time = self.get("time", None)
        if internal_time is not None:
            return datetime.datetime.fromisoformat(internal_time)
        return datetime.datetime.now()

    @time.setter
    def time(self, value: datetime.datetime) -> None:
        self["time"] = value

    @property
    def timestamp(self) -> datetime.datetime | None:
        """The Planhat recorded timestamp for the metric, cannot be set."""
        try:
            internal_timestamp = self.get("timestamp", {}).get("value", None)
        except AttributeError:
            return None
        if internal_timestamp is not None:
            return datetime.datetime.fromisoformat(internal_timestamp)
        return None

    @property
    def parent_id(self) -> str:
        """
        The ID of the parent object that this metric is associated with in Planhat.
        Cannot be set.
        """
        return self.get("parentId", "")

    @property
    def company_name(self) -> str:
        """
        The name of the company that this metric is associated with in Planhat.
        Cannot be set.
        """
        return self.get("companyName", "")


class MetricList(PlanhatListCompanyOwnedMixin[Metric], PlanhatBaseObjectList[Metric]):
    """A list of Planhat metrics."""

    def __init__(self, __iterable: Iterable[Metric] | None = None) -> None:
        """
        Initializes the Planhat list using the provided list of Planhat
        metrics. The type of the first metric in the list is used to
        determine the type of the list.

        Args:
            __iterable: A list of Planhat metrics.
        """
        self._type = Metric
        super().__init__(__iterable)
        self._parent_id_dict: defaultdict[str, MetricList] = defaultdict(
            lambda: MetricList()
        )
        self._parent_id_dict_value_len = 0

    def find_by_parent_id(self, parent_id: str) -> "MetricList":
        """
        Returns the Planhat metrics associated with the provided parent ID.

        Args:
            parent_id: The ID of the parent object.

        Returns:
            A list of Planhat metrics associated with the given parent ID.
        """
        if len(self) == 0:
            raise ValueError(
                f"Cannot find {self._type.__name__} by parent ID because the list is empty."
            )
        if len(self) != self._parent_id_dict_value_len:
            self._parent_id_dict = defaultdict(lambda: MetricList())
            self._parent_id_dict_value_len = 0
        if len(self._parent_id_dict) == 0:
            for item in self:
                self._parent_id_dict[item.parent_id].append(item)
                self._parent_id_dict_value_len += 1
            msg = f"Parent ID dict: {self._parent_id_dict}"
            self.logger.debug(msg)
            log.debug(msg)
        return self._parent_id_dict[parent_id]
