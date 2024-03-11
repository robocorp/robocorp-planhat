from datetime import date
from typing import Type

import requests
from robocorp import log

from . import types
from .errors import PlanhatNotFoundError
from .session import PlanhatSession


class PlanhatClient:
    """
    Automation class to interact with the Planhat API.

    For full documentation of every endpoint, refer to the
    [Planhat API documentation](https://docs.planhat.com).

    This class provides session management and authentication including
    integration with the Robocorp vault as well as generic methods to
    interact with the Planhat API. These methods generally require you
    to provide the `object_type` parameter which is a subclass of
    `PlanhatObject`.

    The `PlanhatClient` class also provides caching of objects. This
    means that if you retrieve a list of objects, they are stored in
    memory and subsequent calls to retrieve the same objects are
    retrieved from the cache. This can be disabled by setting the
    `use_caching` parameter to `False`.

    Note: The Planhat API has a limit of 2000 objects per request for
    most object types. Companies are limited to 5000 objects per request.

    Example:

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
    """

    def __init__(
        self,
        api_key: str | None = None,
        vault_secret_name: str | None = None,
        tenant_uuid: str | None = None,
        use_caching: bool = True,
    ) -> None:
        """
        Initializes the Planhat class. Uses the default secret vault
        object named `planhat_api` unless you provide authentication
        information via the `api_key` and `tenant_uuid` parameters or
        via the `vault_secret_name` parameter. If the latter is provided,
        the vault secret must contain the following keys:

            - `api_key`
            - `tenant_uuid`

        Note: If both `api_key` and `vault_secret_name` are provided,
        `api_key` will be used. And, `tenant_uuid` is only required if
        you need to post analytics data to Planhat.

        Args:
            api_key: The Planhat API key.
            vault_secret_name: The name of the vault secret
                containing the Planhat API key. If you provide an API key,
                this parameter is ignored. The provided vault secret must
                have a key named `api_key`. Defaults to `planhat_api`.
            tenant_uuid: The Planhat tenant UUID.
            use_caching: If `True`, the client will cache all objects
                it retrieves. Defaults to `True`.
        """
        self._session = None
        self.authenticate(api_key, vault_secret_name, tenant_uuid)
        self._cache: dict[type, types.PlanhatObjectList] = {}
        self.use_caching = use_caching

    def authenticate(
        self,
        api_key: str | None = None,
        vault_secret_name: str | None = None,
        tenant_uuid: str | None = None,
    ) -> None:
        """
        Configures session authentication.

        Args:
            api_key: The Planhat API key.
            vault_secret_name: The name of the vault secret
                containing the Planhat API key. If you provide an API key,
                this parameter is ignored. The provided vault secret must
                have a key named `api_key`. Defaults to `planhat_api`.
            tenant_uuid: The Planhat tenant UUID needed to
                post analytics If not provided, the vault object is checked
                for a key named `tenant_uuid`. If the key is not found, the
                tenant UUID is not set and analytics calls will fail.
        """
        if api_key is None and vault_secret_name is None:
            vault_secret_name = "planhat_api"
        self.session.authenticate(api_key, vault_secret_name, tenant_uuid)

    @property
    def session(self) -> PlanhatSession:
        """
        The authenticated requests session.

        Returns:
            PlanhatSession: The authenticated requests session. Raises an exception
                if default authentication is not configured within the vault.
                For custom authentication, use the `authenticate` method first.
        """
        if self._session is None:
            self._session = PlanhatSession()
        return self._session

    @property
    def use_caching(self) -> bool:
        """
        Returns the current cache setting.

        If `True`, the client will cache all objects it retrieves. If `False`,
        the cache is disabled and all objects are retrieved from the Planhat API.
        """
        return self._use_caching

    @use_caching.setter
    def use_caching(self, value: bool) -> None:
        self._use_caching = value
        if not value:
            self._cache = {}

    def _type_check_object_type_param(
        self, object_type: Type[types.PlanhatObject]
    ) -> None:
        """
        Checks if the provided object type is valid.

        Args:
            object_type: The Planhat object type.

        Raises:
            ValueError: If the object type is not valid.
        """
        if not issubclass(object_type, types.PlanhatObject):
            raise ValueError(
                f"{object_type} is not a valid Planhat object type. Valid types are {types.PlanhatObject}"
            )

    def _get_api_name_from_type(self, object_type: Type[types.PlanhatObject]) -> str:
        """
        Gets the API name for the provided object type.

        Args:
            object_type: The Planhat object type.

        Returns:
            str: The API name for the object type.

        Raises:
            ValueError: If the object type does not have an API_NAME defined.
        """
        self._type_check_object_type_param(object_type)
        if object_type.API_NAME is None:
            raise ValueError(f"{object_type} does not have an API_NAME defined.")
        return object_type.API_NAME

    def _build_url_from_id(
        self, object_type: Type[types.PlanhatObject], id: str | None = None
    ) -> str:
        """
        Builds the Planhat URL for the given object type and ID. If
        no ID is provided, the URL for the object type is returned.

        Args:
            object_type: The Planhat object type to use.
            id: The Planhat object ID.

        Returns:
            The Planhat URL for the given object type and ID.
        """
        api_name = self._get_api_name_from_type(object_type)
        if id:
            return f"{api_name}/{id}"
        else:
            return api_name

    def _create_id_parameter(self, id, id_type=None) -> str:
        """
        Creates the ID paramater for a query.

        Args:
            id: The ID to use.
            id_type: The ID type to use. If not provided, the ID is
                used as-is.

        Returns:
            str: The created ID parameter.
        """
        if id_type is not None:
            out = f"{id_type.value}{id}"
        else:
            out = str(id)
        log.debug(f"Created ID parameter: {out}")
        return out

    def _resp_as_singleton(
        self, planhat_response: types.MO | types.PlanhatObjectList[types.MO]
    ) -> types.MO:
        """
        Validates that the response is not a list of Planhat Objects and
        returns it, otherwise raises a ValueError.

        Args:
            planhat_response: The response to validate and return

        Returns:
            The validated response

        Raises:
            ValueError: If the response is a PlanhatObjectList
        """
        if isinstance(planhat_response, types.PlanhatObjectList):
            raise ValueError(
                f"Unexpected response as PlanhatObjectList: {planhat_response}"
            )
        return planhat_response

    def _resp_as_list(
        self, planhat_response: types.MO | types.PlanhatObjectList[types.MO]
    ) -> types.PlanhatObjectList[types.MO]:
        """
        Validates that the response is a list and returns it, if
        a single object is returned, it is wrapped in a list, otherwise
        a ValueError is raised.

        Args:
            planhat_response: The response to validate and return

        Returns:
            The validated response

        Raises:
            ValueError: If the response is not a PlanhatObjectList or
                PlanhatObject
        """
        if isinstance(planhat_response, types.PlanhatObjectList):
            return planhat_response
        elif isinstance(planhat_response, types.PlanhatObject):
            return types.PlanhatObjectList([planhat_response])
        else:
            raise ValueError(f"Unexpected response: {planhat_response}")

    def _get_from_cache(
        self, object_type: type[types.MO]
    ) -> types.PlanhatObjectList[types.MO]:
        """Returns the list of objects from the cache, if available."""
        if object_type not in self._cache:
            object_list = self._get_objects_via_api(object_type)
            self._cache[object_type] = object_list
        return self._cache[object_type]

    def _update_objects_in_cache(self, object_type, objects):
        """
        Updates the object list in the cache.

        Args:
            object_type: The type of the objects being updated.
            objects: The list of objects to update.
        """
        if object_type in self._cache:
            for obj in objects:
                try:
                    existing_obj = self._get_from_cache(object_type).find_by_id(obj.id)
                    existing_obj.update(obj)
                except PlanhatNotFoundError:
                    self._get_from_cache(object_type).append(obj)

    def update_objects(
        self, payload: types.PlanhatObjectList[types.MO]
    ) -> dict | list[dict]:
        """
        Bulk upserts a list of objects to Planhat.

        To decide if an object should be created or updated, Planhat first
        tries to match the object by one of the following keys:

            - `_id` (Planhat native ID)
            - `sourceId` (Source CRM ID)
            - `externalId` (ID in your own system)

        Note: The type of the first object in the payload is used to
        determine the object type. All objects in the payload must be
        of the same type.

        When updating an object, certain properties may not be updated via
        the API, those properties should be removed or never selected when
        retrieving the object.

        Args:
            payload: The PlanhatObjectList to upsert.

        Returns:
            If the length of the payload is greater than 5000, the function
            returns a list of batched responses. Otherwise, it returns a
            single response. The response is a dictionary containing the
            number of objects created and updated, for example:

            {
                "created": 2,
                "createdErrors": [],
                "insertsKeys": [
                    {
                        "_id": "623a1906b4c82d7a1ac76224",
                        "externalId": "test-002"
                    },
                    {
                        "_id": "623a1906b4c82d7a1ac76225",
                        "externalId": "test-003"
                    },
                    ...
                ],
                "updated": 0,
                "updatedErrors": [],
                "updatesKeys": [],
                "nonupdates": 0,
                "modified": [],
                "upsertedIds": [
                    "623a1906b4c82d7a1ac76224",
                    "623a1906b4c82d7a1ac76225",
                    ...
                ],
                "permissionErrors": []
            }

        Example:

            ```python
            updated_objects = types.Company.from_list([
                {"externalId": "test-002", "name": "Test Company 2"},
                {"externalId": "test-003", "name": "Test Company 3"}
            ])
            response = client.update_objects(updated_objects)
            ```
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

    def _bulk_upsert_one_object_batch(self, payload: types.PlanhatObjectList) -> dict:
        response = self.session.put(url=payload.get_urlpath(), data=payload.encode())
        return response.json()

    def _get_objects_via_api(
        self,
        object_type: Type[types.MO],
        company_ids: list[str] | None = None,
        properties: list[str] | None = None,
    ) -> types.PlanhatObjectList[types.MO]:
        """
        Gets a list of planhat objects of `object_type` using the Planhat API.
        This method does not respect the `use_caching` setting and always retrieves
        the objects from the API.

        Args:
            object_type: The type of planhat object to retrieve.
            company_ids: The IDs of the companies to retrieve objects for.
            properties: The properties to include in the retrieved objects.

        Returns:
            A list of planhat objects of the specified `object_type`.
        """
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
            company_ids_batches: list[list[str]] = []
            current_batch: list[str] = []
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
            full_obj_list: types.PlanhatObjectList[types.MO] = types.PlanhatObjectList()
            for company_ids_batch in company_ids_batches:
                current_obj_list = self._get_objects_via_api(
                    object_type=object_type,
                    company_ids=company_ids_batch,
                    properties=properties,
                )
                full_obj_list.extend(current_obj_list)
        else:
            # Code for when the company_ids list is not too long
            ids_string = ",".join(company_ids) if company_ids else None
            properties_string = ",".join(properties) if properties else None
            params: dict[str, int | str] = {"limit": limit}
            if ids_string is not None:
                params["companyId"] = ids_string
            if properties_string is not None:
                params["select"] = properties_string
            full_obj_list = types.PlanhatObjectList()
            for counter in range(1000):
                log.debug(f"Getting {object_type.__name__} batch {counter}")
                bottom = counter * limit
                params["offset"] = bottom
                current_response = self.session.get(
                    url=self._build_url_from_id(object_type), params=params
                )
                found_objs = self._resp_as_list(
                    object_type.from_response(current_response)
                )
                response_length = len(found_objs)
                full_obj_list.extend(found_objs)
                if response_length < limit or response_length == 0:
                    break
        log.debug(f"Found {len(full_obj_list)} objects.")
        if self.use_caching:
            self._update_objects_in_cache(object_type, full_obj_list)
        return full_obj_list

    def get_objects(
        self,
        object_type,
        company_ids=None,
        properties=None,
    ):
        """
        Gets a list of planhat objects of `object_type`.

        This keyword respects the `use_caching` setting and will use the
        cache if enabled, unless the `properties` parameter is provided.

        If no objects are found, a `PlanhatNotFoundError` is raised.

        You can filter the response by `company_ids`. If `company_ids` is `None`,
        all objects of the provided `object_type` are returned up to the
        maximum number of objects allowed by the Planhat API (2000 for most,
        5000 for companies).

        You can define the properties you'd like included using `properties`.
        If `properties` is `None`, only the `_id` and `name` properties
        are returned (or whatever properties are attached to the object in the
        cache). If you want all properties, provide the string
        `ALL` to the `properties` parameter.

        Args:
            object_type: The Planhat object type.
            company_ids: IDs to use to filter the objects. You may provide a single ID
                as a string or a list of IDs. If `None`, all objects are returned.
            properties: Properties to be included in the return object. You may
                provide a single property as a string or a list of properties. If `None`,
                only the `_id` and `name` properties are returned. If you want all
                properties, provide the string `ALL`.

        Returns:
            A list of planhat objects of `object_type` that match the provided filters.

        Raises:
            ValueError: If the object type is not valid.
            PlanhatNotFoundError: If no objects are found.

        Example:

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
        """
        self._type_check_object_type_param(object_type)
        if company_ids is not None and isinstance(company_ids, str):
            company_ids = [company_ids]
        if properties is not None and isinstance(properties, str):
            properties = [properties]
        if self.use_caching and properties is None:
            fetched_objects = []
            try:
                fetched_objects = self._get_from_cache(object_type)
            except KeyError:
                fetched_objects = self._get_objects_via_api(object_type, company_ids)
            if company_ids is None:
                return fetched_objects
            elif object_type is types.Company:
                return_objs = [obj for obj in fetched_objects if obj.id in company_ids]
                misses = [
                    id
                    for id in company_ids
                    if id not in [obj.id for obj in return_objs]
                ]
            else:
                return_objs = [
                    obj for obj in fetched_objects if obj.company_id in company_ids
                ]
                misses = [
                    id
                    for id in company_ids
                    if id not in [obj.company_id for obj in return_objs]
                ]
            if len(misses) == 0:
                return return_objs
            else:
                return_objs.extend(self._get_objects_via_api(object_type, misses))
                return return_objs

        else:
            return self._get_objects_via_api(object_type, company_ids, properties)

    def get_object_by_id(
        self,
        object_type: Type[types.MO],
        id: str,
        id_type: types.PlanhatIdType | None = None,
    ) -> types.MO:
        """
        Gets a planhat object of `object_type` using the provided `id`.

        You can provide alternate ids via the `id_type`. If no object is found,
        `PlanhatNotFoundError` is raised. This method respects the `use_caching`
        setting and will use the cache if enabled.

        Args:
            object_type: The Planhat object type.
            id: The ID to use to find the object.
            id_type: The ID type to use. If not provided, the ID is used as-is.

        Returns:
            The planhat object of `object_type` that matches the provided `id`.

        Raises:
            ValueError: If the object type is not valid.
            PlanhatNotFoundError: If no object is found.

        Example:

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
        """
        if self.use_caching:
            try:
                return self._get_from_cache(object_type).find_by_id_type(id, id_type)
            except PlanhatNotFoundError:
                pass
        id_to_use = self._create_id_parameter(id, id_type)
        response = self.session.get(url=self._build_url_from_id(object_type, id_to_use))
        return self._resp_as_singleton(object_type.from_response(response))

    def create_object(self, payload: types.PlanhatObject) -> types.PlanhatObject:
        """
        Creates a Planhat object.

        Args:
            payload: A PlanhatObject containing the data to create. The
                object must not have a Planhat ID set and must have
                the required fields for the object type. See the Planhat
                API documentation for more information.

        Returns:
            The newly created PlanhatObject.

        Raises:
            PlanhatBadRequestError: If the object already exists.

        Example:

            ```python
            # Create a new company
            new_company = types.Company(name="New Company")
            created_company = client.create_object(new_company)
            ```
        """
        response = self.session.post(
            url=payload.get_type_urlpath(), data=payload.encode()
        )
        return self._resp_as_singleton(types.PlanhatObject.from_response(response))

    def update_object(
        self,
        payload: types.MO,
    ) -> types.MO:
        """
        Updates a Planhat object.

        When updating an object, you must provide the object with the
        updated values. The object must have one of the ID properties
        set. They are used in the order listed and only the first one
        found is used. These properties include `id`, `source_id`, and
        `external_id`. Certain properties may not be updated via the
        API, those properties should be removed or never selected when
        retrieving the object.

        Args:
            payload: A PlanhatObject containing the data to update. The
                object must have one of the ID properties set. They are
                used in the order listed and only the first one found is
                used.

                - id
                - source_id
                - external_id

        Returns:
            The updated PlanhatObject.

        Raises:
            PlanhatNotFoundError: If the object does not exist.

        Example:

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
        """
        response = self.session.put(url=payload.get_urlpath(), data=payload.encode())
        return self._resp_as_singleton(types.PlanhatObject.from_response(response))

    def delete_planhat_object(
        self,
        payload: types.PlanhatObject,
    ) -> requests.Response:
        """
        Deletes a Planhat object.

        If the object does not exist, a PlanhatNotFoundError is raised. This
        behavior can be modified by setting `ignore_errors` to `True`.

        Args:
            payload: A PlanhatObject containing the data to update. The object
                must have one of the ID properties set. They are used in the
                order listed and only the first one found is used. These
                properties include `id`, `source_id`, and `external_id`.
            ignore_errors: If `True`, errors are ignored. Defaults to `False`.

        Returns:
            The response from the Planhat API.

        Raises:
            PlanhatNotFoundError: If the object does not exist.

        Example:

            ```python
            # Delete a company
            company = client.get_object_by_id(object_type=types.Company, id="1")
            client.delete_planhat_object(company)
            ```
        """
        return self.session.delete(url=payload.get_urlpath())

    def list_all_companies(self) -> types.PlanhatObjectList[types.Company]:
        """
        Lists all companies in Planhat using the lean companies endpoint.

        This endpoint returns only the company name and ID. This method does
        not respect the `use_caching` setting and always retrieves the objects
        from the API. Note that this endpoint is not restricted to the usual
        5000 company limit.

        Returns:
            A list of all companies in Planhat with only the company name and ID.
        """
        try:
            all_companies = self._resp_as_list(
                types.Company.from_response(self.session.get(url="/leancompanies"))
            )
        except ValueError as e:
            raise PlanhatNotFoundError("No companies found.") from e
        return all_companies

    def find_missing_objects(
        self, objects: types.PlanhatObjectList[types.MO]
    ) -> types.PlanhatObjectList[types.MO]:
        """
        Finds objects missing in Planhat from the list of objects provided.

        The object's type and the name of the ID field must be provided. This
        method returns those that are missing as a new Planhat Object List.

        Args:
            objects: List of objects to check.

        Returns:
            A new Planhat Object List containing the missing objects.

        Example:

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
        """
        missing_objects = types.PlanhatObjectList[types.MO]()
        for obj in objects:
            all_objects_in_planhat = self._get_from_cache(type(obj))
            if not all_objects_in_planhat.is_obj_in_list(obj):
                missing_objects.append(obj)
        return missing_objects

    def get_dimension_data(
        self,
        company_id: str | None = None,
        dimension_name: str | None = None,
        from_date: int | date | None = None,
        to_date: int | date | None = None,
        limit_length: int | None = None,
    ) -> types.MetricList:
        """
        Gets dimension data from Planhat.

        Unles you provide `limit_length`, this method will paginate
        through all the data available.

        Args:
            company_id: The ID of the company to get dimension data for.
            dimension_name: The name of the dimension to get data for.
            from_day: The start day for the data as the number of days
                since the epoch (1970-01-01) or a date object.
            to_day: The end day for the data as the number of days
                since the epoch (1970-01-01) or a date object.
            limit_length: The maximum number of data points to return.

        Returns:
            A list of dimension data as a MetricList.

        Example:

            ```python
            # Get dimension data for a company
            dimension_data = client.get_dimension_data(
                company_id="1",
                dimension_name="installs",
                from_day=19780,
                to_day=19784,
            )
            ```
        """
        params = {}
        if company_id:
            params["cId"] = company_id
        if dimension_name:
            params["dimid"] = dimension_name
        if from_date:
            if isinstance(from_date, date):
                from_date = (from_date - date(1970, 1, 1)).days
            params["from"] = from_date
        if to_date:
            if isinstance(to_date, date):
                to_date = (to_date - date(1970, 1, 1)).days
            params["to"] = to_date

        dimension_data = types.MetricList()
        offset = 0
        if limit_length and limit_length < 2000:
            limit = limit_length
        else:
            limit = 2000
        while True:
            remaining = limit_length - len(dimension_data) if limit_length else None
            if remaining and remaining < limit:
                limit = remaining
            params["limit"] = limit
            params["offset"] = offset
            response = self.session.get(url="/dimensiondata", params=params)
            fetched_metrics = types.Metric.from_response(response)
            if len(fetched_metrics) == 0:
                break
            dimension_data.extend(fetched_metrics)
            if (
                len(fetched_metrics) < limit
                or limit_length
                and len(fetched_metrics) >= limit_length
            ):
                break
            offset += limit
        return dimension_data
