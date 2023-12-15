from typing import Type
import requests

from robocorp import log

from .errors import PlanhatNotFoundError
from .session import PlanhatSession
from . import types


class PlanhatClient:
    """Automation class to interact with the Planhat API.

    For full documentation of every endpoint, refer to the
    [Planhat API documentation](https://docs.planhat.com).

    This class provides session management and authentication including
    integration with the Robocorp vault as well as
    generic methods to interact with the Planhat API. These methods
    generally require you to provide the `object_type` parameter which
    is a subclass of `PlanhatObject`.
    """

    def __init__(
        self,
        api_key: str | None = None,
        vault_secret_name: str | None = None,
        tenant_uuid: str | None = None,
    ) -> None:
        """Initializes the Planhat class. Uses the default secret vault
        object named `planhat_api` unless you provide authentication
        information via the `api_key` and `tenant_uuid` parameters or
        via the `vault_secret_name` parameter. If the latter is provided,
        the vault secret must contain the following keys:

                - `api_key`
                - `tenant_uuid`

        Note: If both `api_key` and `vault_secret_name` are provided,
        `api_key` will be used. And, `tenant_uuid` is only required if
        you need to post analytics data to Planhat.

        :param api_key: The Planhat API key.
        :param vault_secret_name: The name of the secret in the vault.
        :param tenant_uuid: The Planhat tenant UUID.
        """
        self._session = None
        if (
            api_key is not None
            or vault_secret_name is not None
            or tenant_uuid is not None
        ):
            self.authenticate(api_key, vault_secret_name, tenant_uuid)
        self._object_cache: dict[type, types.PlanhatObjectList] = {}

    def authenticate(
        self,
        api_key: str | None = None,
        vault_secret_name: str | None = None,
        tenant_uuid: str | None = None,
    ) -> None:
        """Configures session authentication.

        :param api_key: The Planhat API key.
        :param vault_secret_name: The name of the vault secret containing the Planhat API key.
            If you provide an API key, this parameter is ignored. The provided vault
            secret must have a key named `api_key`. Defaults to `planhat_api`.
        :param tenant_uuid: The Planhat tenant UUID needed to post analytics If not
            provided, the vault object is checked for a key named `tenant_uuid`. If
            the key is not found, the tenant UUID is not set and analytics calls will
            fail.
        """
        self.session.authenticate(api_key, vault_secret_name, tenant_uuid)

    @property
    def session(self) -> PlanhatSession:
        """Returns the authenticated requests session. Raises an exception
        if default authentication is not configured within the vault.
        For custom authentication, use the `authenticate` method first.
        """
        if self._session is None:
            self._session = PlanhatSession()
        return self._session

    def _type_check_object_type_param(
        self, object_type: Type[types.PlanhatObject]
    ) -> None:
        """Checks if the provided object type is valid.

        :param object_type: The Planhat object type.
        """
        if not issubclass(object_type, types.PlanhatObject):
            raise ValueError(
                f"{object_type} is not a valid Planhat object type. Valid types are {types.PlanhatObject}"
            )

    def _get_api_name_from_type(self, object_type: Type[types.PlanhatObject]) -> str:
        """Gets the API name for the provided object type.

        :param object_type: The Planhat object type.
        """
        self._type_check_object_type_param(object_type)
        if object_type.API_NAME is None:
            raise ValueError(f"{object_type} does not have an API_NAME defined.")
        return object_type.API_NAME

    def _build_url_from_id(
        self, object_type: Type[types.PlanhatObject], id: str | None = None
    ) -> str:
        """Builds the Planhat URL for the given object type and ID. If
        no ID is provided, the URL for the object type is returned.

        :param object_type: The Planhat object type to use
        :param id: The Planhat object ID.
        :returns: The Planhat URL for the given object type and ID.
        """
        api_name = self._get_api_name_from_type(object_type)
        if id:
            return f"{api_name}/{id}"
        else:
            return api_name

    def _create_id_parameter(
        self, id: str, id_type: types.PlanhatIdType | None = None
    ) -> str:
        """Creates the ID paramater for a query based on the provided
        `id` and `id_type`.

        :param id: The ID to use.
        :param id_type: The ID type to use. If not provided, the ID is
            used as-is.
        """
        if id_type is not None:
            out = f"{id_type.value}{id}"
        else:
            out = str(id)
        log.debug(f"Created ID parameter: {out}")
        return out

    def _create_id_parameter_from_object(self, obj: types.PlanhatObject) -> str:
        """Creates the ID paramater for a query based on the provided
        object. Always uses the first ID found in the following order:

            - `id`
            - `source_id`
            - `external_id`

        :param obj: The Planhat object.
        """
        if obj.id:
            id = obj.id
            id_type = types.PlanhatIdType.PLANHAT_ID
        elif obj.source_id:
            id = obj.source_id
            id_type = types.PlanhatIdType.SOURCE_ID
        elif obj.external_id:
            id = obj.external_id
            id_type = types.PlanhatIdType.EXTERNAL_ID
        else:
            raise ValueError("Object must have an id, source_id, or external_id set.")
        return self._create_id_parameter(id, id_type)

    def _resp_as_singleton(
        self, planhat_response: types.PlanhatObject | types.PlanhatObjectList
    ) -> types.PlanhatObject:
        """Validates that the response is a singleton and returns it,
        otherwise raises a ValueError.

        :param planhat_response: The response to validate and return
        """
        if isinstance(planhat_response, types.PlanhatObject):
            return planhat_response
        else:
            raise ValueError(f"Unexpected response: {planhat_response}")

    def _resp_as_list(
        self, planhat_response: types.O | types.PlanhatObjectList[types.O]
    ) -> types.PlanhatObjectList[types.O]:
        """Validates that the response is a list and returns it, if
        a single object is returned, it is wrapped in a list, otherwise
        a ValueError is raised.

        :param planhat_response: The response to validate and return
        """
        if isinstance(planhat_response, types.PlanhatObjectList):
            return planhat_response
        elif isinstance(planhat_response, types.PlanhatObject):
            return types.PlanhatObjectList([planhat_response])
        else:
            raise ValueError(f"Unexpected response: {planhat_response}")

    def _get_object_list_from_cache(
        self, object_type: type[types.O]
    ) -> types.PlanhatObjectList[types.O]:
        """Gets the list of objects from the cache if available."""
        if object_type not in self._object_cache:
            object_list = self.get_objects(object_type)
            self._object_cache[object_type] = object_list
        return self._object_cache[object_type]

    def update_objects(self, payload: types.PlanhatObjectList):
        """Bulk upserts a list of objects to Planhat. The payload must
        be a list of PlanhatObjects.

        To decide if an object should be created or updated, Planhat first
        tries to match the object by one of the following keys:

            - `_id` (Planhat native ID)
            - `sourceId` (Source CRM ID)
            - `externalId` (ID in your own system)

        Note: The type of the first object in the payload is used to
        determine the object type. All objects in the payload must be
        of the same type.

        :param object_type: The Planhat object type.
        :param payload: The PlanhatObjectList to upsert.
        """
        if len(payload) > 5000:
            batched_responses = []
            for counter in range(0, 1000):
                bottom = counter * 5000
                top = bottom + 5000
                response = self._bulk_upsert_one_object_batch(payload[bottom:top])
                batched_responses.append(response)
            return batched_responses
        else:
            response = self._bulk_upsert_one_object_batch(payload)
            return response

    def _bulk_upsert_one_object_batch(self, payload: types.PlanhatObjectList):
        response = self._session.put(url=payload.get_urlpath(), data=payload.encode())
        return response.json()

    def get_objects(
        self,
        object_type: Type[types.O],
        company_ids: str | list | None = None,
        properties: str | list | None = None,
    ) -> types.PlanhatObjectList[types.O]:
        """Gets a list of planhat objects of `object_type`.

        If no objects are found, a `PlanhatNotFoundError` is raised.

        You can filter the response by `company_ids`. If `company_ids` is `None`,
        all objects of the provided `object_type` are returned up to the
        maximum number of objects allowed by the Planhat API (2000 for most,
        5000 for companies).

        You can define the properties you'd like included using `properties`.
        If `properties` is `None`, only the `_id` and `name` properties
        are returned. If you want all properties, provide the string
        `ALL` to the `properties` parameter.

        :param object_type: The Planhat object type.
        :param ids: IDs to use to filter the objects. You may provide a single ID
            as a string or a list of IDs. If `None`, all objects are returned.
        :param properties: Properties to be included in the return object. You may
            provide a single property as a string or a list of properties. If `None`,
            only the `_id` and `name` properties are returned. If you want all
            properties, provide the string `ALL`.
        """
        self._type_check_object_type_param(object_type)
        if company_ids is not None and isinstance(company_ids, str):
            company_ids = [company_ids]
        if properties is not None and isinstance(properties, str):
            properties = [properties]
        log.debug(
            f"Getting '{object_type.__name__}' with ids '{company_ids}' "
            f"and properties '{properties}'"
        )
        if object_type is types.Company:
            limit = 5000
        else:
            limit = 2000

        # Code to handle when the company_ids list is too long
        if company_ids is not None and sum(len(x) for x in company_ids) > 2000:
            # loop through company_ids and get in batches where the total length of the
            # company_ids is less than 2000 characters for each batch
            company_ids_batches = []
            current_batch = []
            current_batch_length = 0
            for company_id in company_ids:
                current_batch_length += len(company_id)
                if current_batch_length > 2000:
                    company_ids_batches.append(current_batch)
                    current_batch = []
                    current_batch_length = len(company_id)
                current_batch.append(company_id)
            company_ids_batches.append(current_batch)
            log.debug(f"Company IDs batches: {company_ids_batches}")
            full_response = types.PlanhatObjectList()
            for company_ids_batch in company_ids_batches:
                current_response = self.get_objects(
                    object_type=object_type,
                    company_ids=company_ids_batch,
                    properties=properties,
                )
                full_response.extend(current_response)
        else:
            # Code for when the company_ids list is not too long
            ids_string = ",".join(company_ids) if company_ids else None
            properties_string = ",".join(properties) if properties else None
            params: dict[str, str | int] = {"limit": limit}
            if ids_string is not None:
                params["companyId"] = ids_string
            if properties_string is not None:
                params["select"] = properties_string
            full_response = types.PlanhatObjectList()
            for counter in range(1000):
                log.debug(f"Getting {object_type.__name__} batch {counter}")
                bottom = counter * limit
                params["offset"] = bottom
                current_response = self._session.get(
                    url=self._build_url_from_id(object_type), params=params
                )
                found_objs = self._resp_as_list(
                    object_type.from_response(current_response)
                )
                response_length = len(found_objs)
                full_response.extend(found_objs)
                if response_length < limit or response_length == 0:
                    break
        if len(full_response) == 0:
            raise PlanhatNotFoundError(
                f"No objects of type '{object_type.__name__}' found with the provided parameters."
            )
        log.debug(f"Found {len(full_response)} objects.")
        return full_response

    # TODO: is the TypeVar needed?
    def get_object_by_id(
        self,
        object_type: Type[types.O],
        id: str,
        id_type: types.PlanhatIdType | None = None,
    ) -> types.O:
        """Gets a planhat object of `object_type` using the provided
        `id`. You can provide alternate ids via the `id_type`. If no
        object is found, `PlanhatNotFoundError` is raised.

        :param object_type: The Planhat object type.
        :param id: The ID to use to find the object.
        :param id_type: The ID type to use. If not provided, the ID is
            used as-is.
        """
        id_to_use = self._create_id_parameter(id, id_type)
        response = self._session.get(
            url=self._build_url_from_id(object_type, id_to_use)
        )
        return self._resp_as_singleton(object_type.from_response(response))

    def create_object(self, payload: types.PlanhatObject) -> types.PlanhatObject:
        """Creates a Planhat object. If the object already exists, a
        PlanhatBadRequestError is raised. Returns the newly created object.

        :param payload: A PlanhatObject containing the data to create. The
            object must not have a Planhat ID set (e.g., `_id` in the
            dictionary). See the full API documentation for the required
            fields for each object type.
        """
        response = self._session.post(
            url=payload.get_type_urlpath(), data=payload.encode()
        )
        return self._resp_as_singleton(types.PlanhatObject.from_response(response))

    def update_object(
        self,
        payload: types.PlanhatObject,
    ) -> types.PlanhatObject:
        """Updates a Planhat object. If the object does not exist, a
        PlanhatNotFoundError is raised.

        :param payload: A PlanhatObject containing the data to update. The
            object must have one of the following ID properties set. They
            are used in the order listed and only the first one found is
            used.

                - `id`
                - `source_id`
                - `external_id`

        :returns: The updated PlanhatObject.
        """
        response = self._session.put(url=payload.get_urlpath(), data=payload.encode())
        return self._resp_as_singleton(types.PlanhatObject.from_response(response))

    def delete_planhat_object(
        self,
        payload: types.PlanhatObject,
    ) -> requests.Response:
        """Deletes a Planhat object. If the object does not exist, a
        PlanhatNotFoundError is raised. You can modify this behavior
        by setting `ignore_errors` to `True`.

        :param payload: A PlanhatObject containing the data to update. The
            object must have one of the following ID properties set. They
            are used in the order listed and only the first one found is
            used.

                - `id`
                - `source_id`
                - `external_id`

        :param ignore_errors: If `True`, errors are ignored. Defaults to `False`.
        :returns: The response from the Planhat API.
        """
        return self._session.delete(url=payload.get_urlpath())

    def list_all_companies(self) -> types.PlanhatObjectList[types.Company]:
        """Lists all companies in Planhat.

        The returned objects will only include the name and ID properties.
        """
        try:
            all_companies = self._resp_as_list(
                types.Company.from_response(self._session.get(url="/leancompanies"))
            )
        except ValueError as e:
            raise PlanhatNotFoundError("No companies found.") from e
        return all_companies

    def find_missing_objects(
        self, objects: types.PlanhatObjectList[types.O]
    ) -> types.PlanhatObjectList[types.O]:
        """Finds objects missing in Planhat from the list of objects provided.
        The object's type and the name of the ID field must be provided.
        Returns those that are missing as a new Planhat Object List.
        """
        missing_objects = types.PlanhatObjectList[types.O]()
        for obj in objects:
            all_objects_in_planhat = self._get_object_list_from_cache(type(obj))
            if not all_objects_in_planhat.is_obj_in_list(obj):
                missing_objects.append(obj)
        return missing_objects
