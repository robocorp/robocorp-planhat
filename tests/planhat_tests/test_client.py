from unittest import mock

import pytest
import responses

from planhat import Planhat, types

# TODO: Implement more complete unit tests


@pytest.fixture
def planhat_client():
    return Planhat(api_key="test_api_key", tenant_uuid="test_tenant_uuid")


@responses.activate
def test_get_companies(planhat_client: Planhat):
    # Mock the response from the Planhat API
    response_json = [
        {"_id": "1", "name": "Test Company 1"},
        {"_id": "2", "name": "Test Company 2"},
    ]
    responses.add(
        responses.GET,
        f"https://api.planhat.com/companies?limit=5000&offset=0",
        json=response_json,
        status=200,
    )

    # Call the method being tested
    companies = planhat_client.get_objects(types.Company)

    # Check that the response was parsed correctly
    assert len(companies) == 2
    assert companies[0].id == "1"
    assert companies[0].name == "Test Company 1"
    assert companies[1].id == "2"
    assert companies[1].name == "Test Company 2"
