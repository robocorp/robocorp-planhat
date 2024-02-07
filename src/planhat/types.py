"""Data types used in the Planhat client."""

from collections import defaultdict
from collections.abc import Iterator
import datetime
import json
import copy
import logging

from urllib import parse
from abc import ABC, abstractproperty
from requests import Response
from enum import Enum
from typing import Any, Iterable, Sequence, SupportsIndex, Type, TypeVar, overload

from robocorp import log  # Remove once logging is integrated into log

from .errors import PlanhatNotFoundError

O = TypeVar("O", bound="PlanhatObject")


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


class PlanhatObject(dict[str, Any], ABC):
    """A base Planhat object. This is a dictionary with some additional
    functionality. The dictionary is the JSON response from Planhat or
    a dictionary containing the Planhat object.
    """

    API_NAME = None
    """The API name for the Planhat object. Used to form the endpoint."""
    SINGULAR = None
    """The singular form of the Planhat object type."""
    PLURAL = None
    """The plural form of the Planhat object type."""

    @classmethod
    def from_response(
        cls: type[O],
        response: Response,
    ) -> "O | PlanhatObjectList[O]":
        """Creates a Planhat object or list of Planhat objects from a
        response from Planhat.

        :param response: The response from Planhat.
        """
        data = response.json()
        if cls is PlanhatObject:
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
    def _extract_type_from_response(cls: type[O], response: Response) -> Type[O]:
        """Extracts the Planhat object type from the request attached to
        the response.
        """

        def _all_subclasses(cls) -> set[type[O]]:
            return set(cls.__subclasses__()).union(
                [s for c in cls.__subclasses__() for s in _all_subclasses(c)]
            )

        _, _, path, _, _ = parse.urlsplit(response.request.url)
        # The third component should reference the endpoint for the object
        # type, because the path should look like "/companies" or "/endusers".
        if isinstance(path, str):
            type_name = path.split("/")[1]
        else:
            raise ValueError(f"Unable to parse path from URL {response.request.url}.")
        # Look through the subclasses and match on API_NAME
        for subclass in _all_subclasses(cls):
            if (
                subclass.API_NAME is not None
                and subclass.API_NAME == type_name
                or subclass.PLURAL is not None
                and subclass.PLURAL == type_name
            ):
                return subclass
        raise ValueError(f"Unable to find Planhat object type for endpoint {path}.")

    @classmethod
    def _from_single_response(cls: type[O], response: Response) -> O:
        """Creates a Planhat object from a response from Planhat.

        :param response: The response from Planhat.
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
        cls: type[O],
        data: list[dict],
    ) -> "PlanhatObjectList[O]":
        """Creates a PlanhatList from a list of dictionaries.

        :param data: A list of dictionaries representing Planhat objects.
        """
        return PlanhatObjectList(cls(item) for item in data)

    @classmethod
    def get_type_urlpath(self) -> str:
        """Returns the URL path for the the object type."""
        return f"/{self.API_NAME}"

    def __init__(
        self,
        data: dict | None = None,
    ):
        """Initializes the Planhat object using the provided dictionary.
        If you want to initialize an object from an API response, use the
        class factory method from_response() instead.

        :param data: A dictionary containing the Planhat object.
        """
        self._response = None
        if data is not None:
            super().__init__(data)
        else:
            super().__init__()

    def __repr__(self) -> str:
        """Returns a string representation of the Planhat object."""
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, source_id={self.source_id}, external_id={self.external_id})"
        )

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

    @property
    def external_id(self) -> str:
        """Returns the external ID of the object."""
        return self.get("externalId", "")

    @property
    def source_id(self) -> str:
        """Returns the source ID of the object."""
        return self.get("sourceId", "")

    @property
    def custom(self) -> dict:
        """Returns the custom fields of the object."""
        return self.get("custom", {})

    def is_same_object(self, other: object) -> bool:
        """Returns whether the other object is the same Planhat object.
        This is determined by comparing the IDs of the objects.
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
        """Returns the URL path for the object utilizing the provided ID type.
        Falls back to any ID type if the provided ID type is not available.

        :param id_type: The ID type to use when generating the URL path.
        """
        if id_type == PlanhatIdType.PLANHAT_ID and self.id:
            return f"/{self.API_NAME}/{self.id}"
        elif id_type == PlanhatIdType.SOURCE_ID and self.source_id:
            return f"/{self.API_NAME}/{id_type.value}{self.source_id}"
        elif id_type == PlanhatIdType.EXTERNAL_ID and self.external_id:
            return f"/{self.API_NAME}/{id_type.value}{self.external_id}"
        else:
            return self._get_any_urlpath()

    def _get_any_urlpath(self) -> str:
        """Returns the URL path for the object utilizing any ID type.
        Always returns an ID based on the following priority:

        1. Planhat ID
        2. Source ID
        3. External ID
        """
        if self.id:
            return self.get_urlpath(PlanhatIdType.PLANHAT_ID)
        elif self.source_id:
            return self.get_urlpath(PlanhatIdType.SOURCE_ID)
        elif self.external_id:
            return self.get_urlpath(PlanhatIdType.EXTERNAL_ID)
        else:
            raise ValueError("Unable to determine ID for object.")

    def _dump(self) -> str:
        """Dumps the object as a JSON string."""
        return json.dumps(self, cls=DateTimeEncoder, allow_nan=False)

    def encode(self) -> bytes:
        """Encodes the object as a byte-like JSON string for API body
        payloads
        """
        return bytes(self._dump(), encoding="utf-8")

    def to_serializable_json(self) -> dict:
        """Return a dictionary where all `datetime` objects within the object
        are converted to ISO 8601 strings.
        """
        # This is a neat trick from the AI, but will it really work?
        return json.loads(self._dump())


class NamedObjectMixin(PlanhatObject, ABC):
    """An abstract class representing objects that have a name."""

    @property
    def name(self) -> str:
        """The name of the object."""
        return self.get("name", "")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name={self.name}, id={self.id}, source_id={self.source_id}, external_id={self.external_id})"
        )


class Company(NamedObjectMixin, PlanhatObject):
    """Companies ("accounts"), are your customers. Depending on your business these might be agencies, schools, other businesses or something else. Companies can also be your previous customers and potentially future customers (prospects).

    The company object is one of the most central in Planhat since most other objects relate to it, and it's frequently used to filter out other information, such as endsuers, licenses, notes etc.

    In Planhat it is possible have a hierarchical structure for the companies, meaning that they can be grouped into organizations with parents and children in a tree like structure.
    """

    API_NAME = "companies"
    SINGULAR = "company"
    PLURAL = "companies"


class PlanhatCompanyOwnedObject(PlanhatObject, ABC):
    """An abstract class representing objects that are owned by a company."""

    @property
    def company_id(self) -> str:
        """The ID of the company that owns this object."""
        return self.get("companyId", self.get("cId", ""))

    @property
    def company_name(self) -> str:
        """The name of the company that owns this object."""
        return self.get("companyName", self.get("cName", ""))


class Asset(PlanhatCompanyOwnedObject):
    """Assets in Planhat can represent many different things depending on your use case. It could be drones, if you're selling a drone tracking product, or it could be instances of your product in cases where a single customer can run multiple instances of your product in parallel. Assets could also represent your different products.

    More generally, Assets are "nested objects" for which you may want to track usage separately, but don't need to treat them as separate customers with individual contacts, conversations, etc.
    """

    API_NAME = "assets"
    SINGULAR = "asset"
    PLURAL = "assets"


class Campaign(PlanhatCompanyOwnedObject):
    """Manage campaigns you are running inside companies, e.g., to drive adoption or to deepen stakeholder relations."""

    API_NAME = "campaigns"
    SINGULAR = "campaign"
    PLURAL = "campaigns"


class Churn(PlanhatCompanyOwnedObject):
    """Each time one of your customers churns or downgrades you can add a specific log about this. Mostly this "churn log" is added manually by the CSM from within Planhat, but there may also be times when you want to add it over API, for example if you're capturing information about downgrades and churn natively in-app in your own platform and want to send that over to Planhat.

    The churn logs in Planhat typically contain the reasons for the churn, the value, date etc. It's important to note though that it doesn't affect actual revenue numbers and KPIs such as churn rate, renewal rate etc, on it's own. Those calculations are entirely based on underlying license data.
    """

    API_NAME = "churn"
    SINGULAR = "churn"
    PLURAL = "churns"


class Conversation(PlanhatCompanyOwnedObject):
    """Conversations can be of different types such as email, chat, support tickets and manually logged notes. You can also create your own types in Planhat to represent things such as "in person meeting", "Training" etc. The default types (email, chat, ticket, call) are reserved and should not be created over API."""

    API_NAME = "conversations"
    SINGULAR = "conversation"
    PLURAL = "conversations"


class CustomField(PlanhatObject):
    """Most objects in Planaht can be customized by creating your own custom fields. Which model a given custom fields belongs is indicated by the parent property.

    Typically you would create the custom fields from within the Planhat app. But in some special cases you may find it more convenient to manage over API instead.
    """

    API_NAME = "customfields"
    SINGULAR = "custom field"
    PLURAL = "custom fields"

    @property
    def parent(self) -> str:
        """The singular name of the parent model which owns this custom field"""
        return self.get("parent", "")


class Enduser(PlanhatCompanyOwnedObject):
    """An enduser represents an individual at one of your customers, typically a user of your product, a business contact or both. Endusers can automatically be created based on user tracking events, or based on conversations such as emails and tickets.

    Often this automatic creation of contacts along with sync from an external CRM or similar is enough. But there are also situations where you may want to be 100% sure all your users exist in Planhat, and then it would make sense to create them in Planhat over api as soon as they get created in your own system.

    If companyId is not present in the payload, and the email has a domain already registered within a company, then Planhat will auto-assign the new enduser to the company using domain matching.
    """

    API_NAME = "endusers"
    SINGULAR = "enduser"
    PLURAL = "endusers"

    @property
    def email(self) -> str:
        """The email address of the enduser."""
        return self.get("email", "")


class Invoice(PlanhatCompanyOwnedObject):
    """Invoices are normally generated automatically in Planhat when a license is created or renewed, invoices can include multiple line items. Planhat will not prepare invoices that you actually can send to your customers though. They're rather meant to help anyone working with your customers to know the status of current and past invoicing.

    Invoices default date fields format should be days format integer. (Days since January 1, 1970, Unix epoch)
    """

    API_NAME = "invoices"
    SINGULAR = "invoice"
    PLURAL = "invoices"


class Issue(PlanhatObject):
    """Issues typically represent Bugs or Feature Requests. Many of our customers fetch issues from Jira, but they can also be pushed to Planhat from other product management tools such as Product Board or Aha! You can also manage issues directly in Planhat without any external tool. Just keep in mind that the functionality is basic and mostly intended to contribute to the customer 360 view.

    Issues in Planhat can link to multiple companies, to multiple endusers and to multiple conversations.
    """

    API_NAME = "issues"
    SINGULAR = "issue"
    PLURAL = "issues"

    @property
    def company_ids(self) -> list[str]:
        """The IDs of the companies that this issue is linked to."""
        return self.get("companyIds", [])

    @property
    def company_names(self) -> list[str]:
        """The names of the companies that this issue is linked to."""
        return self.get("companies", [])

    @property
    def enduser_ids(self) -> list[str]:
        """The IDs of the endusers that this issue is linked to."""
        return self.get("enduserIds", [])

    @property
    def enduser_names(self) -> list[str]:
        """The names of the endusers that this issue is linked to."""
        return self.get("endusers", [])


class License(PlanhatCompanyOwnedObject):
    """Licenses represent your customers' subcriptions to your service and is the base for MRR (or ARR) calculations and most revenue reports. For non recurring revenue, please see the Sale (NRR) object. There are many ways to get license data into Planhat including incomming webhooks and CRM integrations. In some case though, you just want to handle it yourself over the api, for example if the main source of license data is your own system.

    Licenses in Planhat can be fixed period with a defined start and end date. Or they can be non fixed period (sometimes called open-ended or evergreen). Open ended licenses initially don't have a specified end date since the customer may cancel at any time.. once the license is churned/lost also non fixed period licenses can have an end date.
    """

    API_NAME = "licenses"
    SINGULAR = "license"
    PLURAL = "licenses"


class Note(Conversation):
    """Notes in Planhat are technically Conversations. You can create your own custom Touch Types to easily distinguish between different types of notes. You can also use custom fields to add more nuance to your Notes.

    It's quite common for Notes in Planhat to sync with external systems such as Salesforce, Notes can also be created via Zapier or Planhats's native incoming webhooks.
    """

    pass


class NPS(PlanhatCompanyOwnedObject):
    """NPS records in Planhat represent the individual responses to an nps survey. Typically these are created automatically when running an nps campaign in Planhat, or in some cases imported from external NPS tools. A single enduser/contact can have multiple records if they responded to different surveys over time.

    Based on the NPS records each enduser and company in Planhat also get an nps score assigned.
    """

    API_NAME = "nps"
    SINGULAR = "nps"
    PLURAL = "nps"

    @property
    def campaign_id(self) -> str:
        """The ID of the campaign that this NPS record is linked to."""
        return self.get("campaignId", "")


class Opportunity(PlanhatCompanyOwnedObject):
    """Opportunities in Planhat represent a sales opportunity, whether it's selling to a new customer or more commonly a chance of expanding an existing account.

    Opportunities are not the sames as Licenses, but when an opportunity is closed won in Planhat, there is an optional setting to generate a licenses based on the opportunity data.
    """

    API_NAME = "opportunities"
    SINGULAR = "opportunity"
    PLURAL = "opportunities"


class Objective(PlanhatCompanyOwnedObject):
    """Being very clear and focused on your goals with customers is critical, and now you can track objectives and the health per objective.

    Pro-tip: use your average Objective health in the Health Score!
    """

    API_NAME = "objectives"
    SINGULAR = "objective"
    PLURAL = "objectives"


class Project(PlanhatCompanyOwnedObject):
    """Projects can represent many different real world objects with a natural start and stop date. A service provider for schools may use Projects to represent classes or courses. If you're selling a software to run sales competitions, then each competition may be a project.

    Using custom fields you can tailor projects to your needs, and just like Assets, usage data and time series data (metrics) can be associated with your Projetcs.
    """

    API_NAME = "projects"
    SINGULAR = "project"
    PLURAL = "projects"


class Sale(PlanhatCompanyOwnedObject):
    """The Sale (NRR) model represents not recurring revenue, like an onboarding fee, or a one-off professional services project."""

    API_NAME = "sales"
    SINGULAR = "sale"
    PLURAL = "sales"


class Task(PlanhatCompanyOwnedObject):
    """Tasks are the things that you plan to do in the future. It can be a simple "to-do" without any specific due date, a reminder of something to be done at a specific point in time, or even a meeting with a start and end time.

    Most of the time these tasks will be automatically generated in Planhat based on rules you set up. It's also comon to have tasks as steps in a Playbook. But tasks can also be created ad-hoc just like you would in any task management app.

    Tasks managed over the API should typically have the mainType property set to `task`, the other potential value is `event`, which indicates that it was synced to or from a calendar like Google Calendar. Though it's also possible to create tasks of type event in Planhat without syncing them back to any calendar.

    Once a task is completed it's archived and genrally not visble in Planhat anymore. Sometimes when completing a tasks, say a training session, you want to log a note summarizing how it went, this is managed automatically by Planhat when working in the Planhat app.
    """

    API_NAME = "tasks"
    SINGULAR = "task"
    PLURAL = "tasks"

    @property
    def task_type(self) -> str:
        """The type of task that this task is."""
        return self.get("type", "")


class Ticket(PlanhatCompanyOwnedObject):
    """Tickets in Planhat are Conversations, so if you plan to send tickets to Planhat via API then you can also use that endpoint. The ticket endpoint contains a bit of convenience logic for save tickets specificially, like setting the proper type automatically.

    Most of our customers sync tickets from an external system like Zendesk or Salesforce. In case your ticketing system isn't natively supported or you have your own system for it, please let us know and we'll be happy to discuss how to best work with this api.
    """

    API_NAME = "tickets"
    SINGULAR = "ticket"
    PLURAL = "tickets"

    @property
    def email(self) -> str:
        """The email address of user who submitted the ticket."""
        return self.get("email", "")


class User(PlanhatObject):
    """Users are all your team members that need access to Planhat. Users can be created in the app, using spreadsheet upload or over api. If you're using teams to group your users in Planhat you'll need to call a separate endpoint to associate your Users with the right teams.

    If a user is flagged as inactive, they will not be able to login to Planhat and they will not get notifications, but they will be available for assigning accounts etc.
    """

    API_NAME = "users"
    SINGULAR = "user"
    PLURAL = "users"

    @property
    def email(self) -> str:
        """The email address of the user."""
        return self.get("email", "")

    @property
    def first_name(self) -> str:
        """The first name of the user."""
        return self.get("firstName", "")

    @property
    def last_name(self) -> str:
        """The last name of the user."""
        return self.get("lastName", "")


class Workspace(PlanhatCompanyOwnedObject):
    """If you work with sub-instances at your customers, e.g., connecting with different departments or with different versions of your product (think like a Workspace in Slack), then this is the object to track that engagement!"""

    API_NAME = "workspaces"
    SINGULAR = "workspace"
    PLURAL = "workspaces"

    @property
    def name(self) -> str:
        """The name of the workspace."""
        return self.get("name", "")


class PlanhatObjectList(list[O]):
    """A list of Planhat objects."""

    def __init__(self, __iterable: Iterable[O] | None = None) -> None:
        """Initializes the Planhat list using the provided list of Planhat
        objects. The type of the first object in the list is used to
        determine the type of the list.

        :param data: A list of Planhat objects.
        """
        if __iterable is None:
            __iterable = []
        super().__init__(__iterable)
        if len(self) > 0:
            self._type = type(self[0])
        else:
            self._type = PlanhatObject
        self._validate()
        self._id_dict = {}
        self._source_id_dict = {}
        self._external_id_dict = {}
        self._company_id_dict = defaultdict(PlanhatObjectList[O])
        self._company_id_dict_value_len = 0
        self.logger = logging.getLogger(__name__)

    def _set_type_if_not_set(
        self, obj: "O | PlanhatObjectList[O] | Sequence[O]"
    ) -> None:
        """Sets the type of the list if it has not been set yet."""
        if self._type is PlanhatObject:
            if isinstance(obj, PlanhatObject):
                self._type = type(obj)
            elif isinstance(obj, PlanhatObjectList):
                if len(obj) > 0:
                    self._type = type(obj[0])
            elif isinstance(obj, Sequence):
                if len(obj) > 0:
                    self._type = type(obj[0])

    def _validate(self) -> None:
        """Validates the list of Planhat objects."""
        for index, obj in enumerate(self):
            if not isinstance(obj, self._type):
                raise TypeError(
                    f"Expected PlanhatObject, got {type(obj).__name__} instead at index {index}."
                )

    @overload
    def __getitem__(self, key: SupportsIndex) -> O: ...

    @overload
    def __getitem__(self, key: slice) -> "PlanhatObjectList[O]": ...

    def __getitem__(self, key: SupportsIndex | slice) -> "O | PlanhatObjectList[O]":
        """Returns a Planhat object or PlanhatObjectList."""
        if isinstance(key, slice):
            return PlanhatObjectList(super().__getitem__(key))
        else:
            return super().__getitem__(key)

    @overload
    def __setitem__(self, key: SupportsIndex, value: O) -> None: ...

    @overload
    def __setitem__(self, key: slice, value: "PlanhatObjectList[O]") -> None: ...

    @overload
    def __setitem__(self, key: SupportsIndex, value: Sequence[O]) -> None: ...

    def __setitem__(
        self,
        key: SupportsIndex | slice,
        value: "O | PlanhatObjectList[O] | Sequence[O]",
    ) -> None:
        """Sets a Planhat object or list of Planhat objects."""
        if len(self) == 0:
            self._set_type_if_not_set(value)
        if isinstance(key, slice):
            if isinstance(value, self._type):
                raise TypeError(
                    f"Expected PlanhatObjectList[{self._type}] or Sequence[{self._type}], "
                    f"got {type(value).__name__} instead."
                )
            super().__setitem__(key, value)
        else:
            if not isinstance(value, self._type):
                raise TypeError(
                    f"Expected {self._type}, got {type(value).__name__} instead."
                )
            super().__setitem__(key, value)
        self._validate()

    def __iter__(self) -> Iterator[O]:
        return super().__iter__()

    def append(self, obj: O) -> None:
        """Appends a Planhat object to the list."""
        if len(self) == 0:
            self._set_type_if_not_set(obj)
        if not isinstance(obj, self._type):
            raise TypeError(f"Expected {self._type}, got {type(obj).__name__} instead.")
        super().append(obj)

    @overload
    def extend(self, objs: "PlanhatObjectList[O]") -> None: ...

    @overload
    def extend(self, objs: Sequence[O]) -> None: ...

    def extend(self, objs: "PlanhatObjectList[O] | Sequence[O]") -> None:
        """Extends the list with a list of Planhat objects."""
        if len(self) == 0:
            self._set_type_if_not_set(objs)
        if not isinstance(objs, PlanhatObjectList):
            objs = PlanhatObjectList(objs)
        super().extend(objs)
        self._validate()

    def insert(self, index: SupportsIndex, obj: O) -> None:
        """Inserts a Planhat object at the provided index."""
        if not isinstance(obj, PlanhatObject):
            raise TypeError(
                f"Expected PlanhatObject, got {type(obj).__name__} instead."
            )
        super().insert(index, obj)

    def remove(self, obj: O) -> None:
        """Removes a Planhat object from the list."""
        if not isinstance(obj, self._type):
            raise TypeError(f"Expected {self._type}, got {type(obj).__name__} instead.")
        super().remove(obj)

    def is_obj_in_list(self, obj: O) -> bool:
        """Returns whether the provided Planhat object is in the list
        based on IDs."""
        if not isinstance(obj, self._type):
            raise TypeError(f"Expected {self._type}, got {type(obj).__name__} instead.")
        for item in self:
            if item.is_same_object(obj):
                return True
        return False

    def find_by_id(self, id: str) -> O:
        """Returns the Planhat object with the provided ID."""
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

    def find_by_source_id(self, source_id: str) -> O:
        """Returns the Planhat objects with the provided source ID."""
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

    def find_by_external_id(self, external_id: str) -> O:
        """Returns the Planhat objects with the provided external ID."""
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

    def find_by_id_type(self, id: str, id_type: PlanhatIdType) -> O:
        """Returns the Planhat object with the provided ID type."""
        if id_type == PlanhatIdType.PLANHAT_ID:
            return self.find_by_id(id)
        elif id_type == PlanhatIdType.SOURCE_ID:
            return self.find_by_source_id(id)
        elif id_type == PlanhatIdType.EXTERNAL_ID:
            return self.find_by_external_id(id)
        else:
            raise ValueError(f"Invalid ID type: {id_type}.")

    def find_by_company_id(self, company_id: str) -> "PlanhatObjectList[O]":
        """Returns the Planhat objects with the provided company ID."""
        if len(self) != self._company_id_dict_value_len:
            self._company_id_dict = defaultdict(PlanhatObjectList[O])
            self._company_id_dict_value_len = 0
        if len(self._company_id_dict) == 0:
            for item in self:
                if isinstance(item, PlanhatCompanyOwnedObject):
                    self._company_id_dict[item.company_id].append(item)
                    self._company_id_dict_value_len += 1
                else:
                    raise TypeError(
                        f"Cannot find {self._type.__name__} by company ID because it "
                        f"is not a company-owned object."
                    )
            msg = f"Company ID dict: {self._company_id_dict}"
            self.logger.debug(msg)
            log.debug(msg)  # Remove once logging is integrated into log
        return self._company_id_dict[company_id]

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
        if self._type is not PlanhatObject:
            return f"/{self._type.API_NAME}"
        else:
            raise ValueError("Unable to determine URL path for list with no set type.")
