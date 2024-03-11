from datetime import date
import datetime
import pytest
import responses

from planhat import Planhat, errors, types


class TestWithoutCache:
    @pytest.fixture
    def planhat(self, planhat_client: Planhat):
        planhat_client.use_caching = False
        return planhat_client

    @responses.activate
    def test_get_companies(self, planhat: Planhat):
        # Mock the response from the Planhat API
        response_json = [
            {"_id": "1", "name": "Test Company 1"},
            {"_id": "2", "name": "Test Company 2"},
        ]
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies?limit=5000&offset=0",
            json=response_json,
            status=200,
        )

        # Call the method being tested
        companies = planhat.get_objects(types.Company)

        # Check that the response was parsed correctly
        assert len(companies) == 2
        assert companies[0].id == "1"
        assert companies[0].name == "Test Company 1"
        assert companies[1].id == "2"
        assert companies[1].name == "Test Company 2"

    @responses.activate
    def test_get_company_by_id(self, planhat: Planhat):
        response_json = {"_id": "1", "name": "Test Company 1"}
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies/1",
            json=response_json,
            status=200,
        )

        company = planhat.get_object_by_id(types.Company, "1")

        assert company.id == "1"
        assert company.name == "Test Company 1"

    @responses.activate
    def test_get_company_by_external_id(self, planhat: Planhat):
        response_json = {"_id": "1", "name": "Test Company 1", "externalId": "1a"}
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies/extid-1a",
            json=response_json,
            status=200,
        )

        company = planhat.get_object_by_id(
            types.Company, "1a", types.PlanhatIdType.EXTERNAL_ID
        )

        assert company.id == "1"
        assert company.name == "Test Company 1"

    @responses.activate
    def test_get_one_company_via_get_objects(self, planhat: Planhat):
        response_json = {"_id": "1", "name": "Test Company 1"}
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies?limit=5000&offset=0&companyId=1",
            json=response_json,
            status=200,
        )

        companies = planhat.get_objects(types.Company, company_ids=["1"])

        assert len(companies) == 1
        assert companies[0].id == "1"
        assert companies[0].name == "Test Company 1"

    @responses.activate
    def test_company_not_found(self, planhat: Planhat):
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies/2",
            status=404,
        )

        with pytest.raises(errors.PlanhatNotFoundError):
            planhat.get_object_by_id(types.Company, "2")

    @responses.activate
    def test_company_not_found_all(self, planhat: Planhat):
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies?limit=5000&offset=0&companyId=2",
            status=404,
        )
        with pytest.raises(errors.PlanhatNotFoundError):
            planhat.get_objects(types.Company, company_ids=["2"])


class TestWithCache:
    @pytest.fixture
    def planhat(self, planhat_client: Planhat) -> Planhat:
        planhat_client.use_caching = True
        return planhat_client

    @pytest.fixture
    @responses.activate
    def planhat_with_company_cache(self, planhat: Planhat) -> Planhat:
        response_json = [
            {"_id": "1", "name": "Test Company 1"},
            {"_id": "2", "name": "Test Company 2"},
        ]
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies?limit=5000&offset=0",
            json=response_json,
            status=200,
        )
        planhat.get_objects(types.Company)
        return planhat

    def test_company_cache_by_id(self, planhat_with_company_cache: Planhat):
        # No mocks used proves that the cache is being used
        single_company = planhat_with_company_cache.get_object_by_id(types.Company, "2")
        assert single_company.id == "2"
        assert single_company.name == "Test Company 2"

    def test_company_cache_all(self, planhat_with_company_cache: Planhat):
        # No mocks used proves that the cache is being used
        companies = planhat_with_company_cache.get_objects(types.Company)
        assert len(companies) == 2
        assert companies[0].id == "1"
        assert companies[0].name == "Test Company 1"
        assert companies[1].id == "2"
        assert companies[1].name == "Test Company 2"

    @responses.activate
    def test_updating_cache(self, planhat_with_company_cache: Planhat):
        response_json = {"_id": "3", "name": "Test Company 3"}
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies?limit=5000&offset=0&companyId=3",
            json=response_json,
            status=200,
        )
        planhat_with_company_cache.get_objects(types.Company, company_ids=["3"])
        # Confirm that the cache has been updated
        company = planhat_with_company_cache.get_object_by_id(types.Company, "3")
        assert company.id == "3"
        assert company.name == "Test Company 3"

    @responses.activate
    def test_updating_existing_company_in_cache(
        self, planhat_with_company_cache: Planhat
    ):
        response_json = {
            "_id": "2",
            "name": "Test Company 2 Updated",
            "custom": {"field": "value"},
        }
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies?limit=5000&offset=0&companyId=2&select=name,custom",
            json=response_json,
            status=200,
        )
        planhat_with_company_cache.get_objects(
            types.Company, company_ids=["2"], properties=["name", "custom"]
        )
        # Confirm that the cache has been updated
        company = planhat_with_company_cache.get_object_by_id(types.Company, "2")

        assert company.id == "2"
        assert company.name == "Test Company 2 Updated"
        assert company.custom == {"field": "value"}

    @responses.activate
    def test_cache_not_found_by_id(self, planhat_with_company_cache: Planhat):
        response_json = {"_id": "4", "name": "Test Company 4"}
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies/4",
            json=response_json,
            status=200,
        )

        company = planhat_with_company_cache.get_object_by_id(types.Company, "4")

        assert company.id == "4"
        assert company.name == "Test Company 4"

    @responses.activate
    def test_cache_not_found_all(self, planhat_with_company_cache: Planhat):
        response_json = [
            {"_id": "3", "name": "Test Company 3"},
            {"_id": "4", "name": "Test Company 4"},
        ]
        responses.add(
            responses.GET,
            "https://api.planhat.com/companies?limit=5000&offset=0&companyId=3,4",
            json=response_json,
            status=200,
        )

        companies = planhat_with_company_cache.get_objects(
            types.Company, company_ids=["3", "4"]
        )

        assert len(companies) == 2
        assert companies[0].id == "3"
        assert companies[0].name == "Test Company 3"
        assert companies[1].id == "4"
        assert companies[1].name == "Test Company 4"

    def test_find_missing_objects(self, planhat_with_company_cache: Planhat):
        missing_objects_to_find = types.PlanhatObjectList(
            [types.Company(id="1"), types.Company(id="11"), types.Company(id="12")]
        )
        missing_objects = planhat_with_company_cache.find_missing_objects(
            missing_objects_to_find
        )
        assert len(missing_objects) == 2
        assert missing_objects[0].id == "11"
        assert missing_objects[1].id == "12"


class TestUncachedMethods:
    @responses.activate
    def test_update_company(self, planhat_client: Planhat):
        response_json = {"_id": "1", "name": "Test Company 1"}
        responses.add(
            responses.PUT,
            "https://api.planhat.com/companies/1",
            json=response_json,
            status=200,
        )

        company_to_update = types.Company({"_id": "1", "name": "Test Company 1"})
        company = planhat_client.update_object(company_to_update)

        assert company.id == "1"
        assert company.name == "Test Company 1"

    @responses.activate
    def test_update_companies(self, planhat_client: Planhat):
        response_json = {
            "created": 2,
            "createdErrors": [],
            "insertsKeys": [
                {"_id": "1", "externalId": "1a"},
                {"_id": "1", "externalId": "2a"},
            ],
            "updated": 0,
            "updatedErrors": [],
            "updatesKeys": [],
            "nonupdates": 0,
            "modified": [],
            "upsertedIds": ["1", "1"],
            "permissionErrors": [],
        }
        responses.add(
            responses.PUT,
            "https://api.planhat.com/companies",
            json=response_json,
            status=200,
        )

        companies_to_update = types.PlanhatObjectList(
            [
                types.Company(external_id="1a", name="Test Company 1"),
                types.Company(external_id="2a", name="Test Company 2"),
            ]
        )
        response = planhat_client.update_objects(companies_to_update)

        assert response == response_json

    @responses.activate
    def test_create_company(self, planhat_client: Planhat):
        response_json = {"_id": "1", "name": "Test Company 1"}
        responses.add(
            responses.POST,
            "https://api.planhat.com/companies",
            json=response_json,
            status=200,
        )

        company_to_create = types.Company(name="Test Company 1")
        company = planhat_client.create_object(company_to_create)

        assert company.id == "1"
        assert company.name == "Test Company 1"

    @responses.activate
    def test_delete_company(self, planhat_client: Planhat):
        response_json = {"n": 1, "ok": 1, "deletedCount": 1}
        responses.add(
            responses.DELETE,
            "https://api.planhat.com/companies/1",
            json=response_json,
            status=200,
        )

        company_to_delete = types.Company(id="1")

        response = planhat_client.delete_planhat_object(company_to_delete)

        assert response.json() == response_json

    @responses.activate
    def test_list_all_companies(self, planhat_client: Planhat):
        response_json = [
            {
                "_id": "1",
                "name": "Test Company 1",
                "externalId": "1a",
                "sourceId": "a1",
            },
            {
                "_id": "2",
                "name": "Test Company 2",
                "externalId": "2a",
                "sourceId": "a2",
            },
        ]
        responses.add(
            responses.GET,
            "https://api.planhat.com/leancompanies",
            json=response_json,
            status=200,
        )

        companies = planhat_client.list_all_companies()

        assert len(companies) == 2
        assert companies[0].id == "1"
        assert companies[0].name == "Test Company 1"
        assert companies[0].external_id == "1a"
        assert companies[0].source_id == "a1"
        assert companies[1].id == "2"
        assert companies[1].name == "Test Company 2"
        assert companies[1].external_id == "2a"
        assert companies[1].source_id == "a2"

    def test_improper_type_parameter(self, planhat_client: Planhat):
        class TestType(object):
            pass

        with pytest.raises(
            ValueError, match="is not a valid Planhat object type. Valid types are"
        ):
            planhat_client.get_objects(TestType)

    def test_no_api_name(self, planhat_client: Planhat):
        class TestType(types.PlanhatObject):
            API_NAME = None

        with pytest.raises(ValueError, match="does not have an API_NAME defined"):
            planhat_client.get_object_by_id(TestType, "1")


class TestMetrics:
    @responses.activate
    def test_get_metrics(self, planhat_client: Planhat):
        response_json = [
            {
                "_id": "1",
                "dimensionId": "test-dimension-id",
                "companyId": "1",
                "time": "2024-02-29T00:00:00.000Z",
                "date": "2024-02-29T00:00:00.000Z",
                "day": 19782,
                "value": 100,
                "timestamp": {
                    "value": "2024-02-29T00:00:00.000Z",
                },
                "model": "Company",
                "parentId": "1",
                "companyName": "Acme",
            },
            {
                "_id": "2",
                "dimensionId": "test-dimension-id",
                "companyId": "1",
                "time": "2024-02-29T00:00:00.000Z",
                "date": "2024-02-29T00:00:00.000Z",
                "day": 19782,
                "value": 100,
                "timestamp": {
                    "value": "2024-02-29T00:00:00.000Z",
                },
                "model": "Asset",
                "parentId": "1a",
                "companyName": "Acme",
            },
        ]
        responses.add(
            responses.GET,
            "https://api.planhat.com/dimensiondata?limit=2000&offset=0",
            json=response_json,
            status=200,
        )

        metrics = planhat_client.get_dimension_data()

        test_datetime = datetime.datetime(
            2024, 2, 29, 0, 0, tzinfo=datetime.timezone.utc
        )
        test_date = date(2024, 2, 29)

        assert len(metrics) == 2
        assert metrics[0].id == "1"
        assert metrics[0].dimension_id == "test-dimension-id"
        assert metrics[0].company_id == "1"
        assert metrics[0].time == test_datetime
        assert metrics[0].date == test_date
        assert metrics[0].day == 19782
        assert metrics[0].value == 100
        assert metrics[0].timestamp == test_datetime
        assert metrics[0].model == "Company"
        assert metrics[0].parent_id == "1"
        assert metrics[0].company_name == "Acme"
        assert metrics[1].id == "2"
        assert metrics[1].dimension_id == "test-dimension-id"
        assert metrics[1].company_id == "1"
        assert metrics[1].time == test_datetime
        assert metrics[1].date == test_date
        assert metrics[1].day == 19782
        assert metrics[1].value == 100
        assert metrics[1].timestamp == test_datetime
        assert metrics[1].model == "Asset"
        assert metrics[1].parent_id == "1a"
        assert metrics[1].company_name == "Acme"

    @responses.activate
    def test_get_metrics_with_params(self, planhat_client: Planhat):
        response_json = [
            {
                "_id": "1",
                "dimensionId": "test-dimension-id-2",
                "companyId": "1",
                "time": "2024-01-10T00:00:00.000Z",
                "date": "2024-01-10T00:00:00.000Z",
                "day": 19732,
                "value": 100,
                "timestamp": {
                    "value": "2024-01-10T00:00:00.000Z",
                },
                "model": "Company",
                "parentId": "1",
                "companyName": "Acme",
            },
            {
                "_id": "2",
                "dimensionId": "test-dimension-id-2",
                "companyId": "1",
                "time": "2024-01-10T00:00:00.000Z",
                "date": "2024-01-10T00:00:00.000Z",
                "day": 19732,
                "value": 100,
                "timestamp": {
                    "value": "2024-01-10T00:00:00.000Z",
                },
                "model": "Asset",
                "parentId": "1a",
                "companyName": "Acme",
            },
        ]
        responses.add(
            responses.GET,
            "https://api.planhat.com/dimensiondata?limit=2000&offset=0&cId=1&"
            "dimid=test-dimension-id-2&from=19732&to=19732",
            json=response_json,
            status=200,
        )

        metrics = planhat_client.get_dimension_data(
            "1",
            "test-dimension-id-2",
            date(2024, 1, 10),
            date(2024, 1, 10),
        )

        test_datetime = datetime.datetime(
            2024, 1, 10, 0, 0, tzinfo=datetime.timezone.utc
        )
        test_date = date(2024, 1, 10)

        assert len(metrics) == 2
        assert metrics[0].id == "1"
        assert metrics[0].dimension_id == "test-dimension-id-2"
        assert metrics[0].company_id == "1"
        assert metrics[0].time == test_datetime
        assert metrics[0].date == test_date
        assert metrics[0].day == 19732
        assert metrics[0].value == 100
        assert metrics[0].timestamp == test_datetime
        assert metrics[0].model == "Company"
        assert metrics[0].parent_id == "1"
        assert metrics[0].company_name == "Acme"
        assert metrics[1].id == "2"
        assert metrics[1].dimension_id == "test-dimension-id-2"
        assert metrics[1].company_id == "1"
        assert metrics[1].time == test_datetime
        assert metrics[1].date == test_date
        assert metrics[1].day == 19732
        assert metrics[1].value == 100
        assert metrics[1].timestamp == test_datetime
        assert metrics[1].model == "Asset"
        assert metrics[1].parent_id == "1a"
        assert metrics[1].company_name == "Acme"
