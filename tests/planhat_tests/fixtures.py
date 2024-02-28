import pytest

from planhat import Planhat


@pytest.fixture
def planhat_client():
    return Planhat(api_key="test_api_key", tenant_uuid="test_tenant_uuid")
