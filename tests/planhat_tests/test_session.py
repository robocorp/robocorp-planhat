from requests.models import PreparedRequest

from planhat.session import PlanhatAuth


def test_auth_header():
    token = "my-token"
    auth = PlanhatAuth(token)

    req = PreparedRequest()
    req.headers = {}
    req = auth(req)

    assert req.headers["Authorization"] == f"Bearer {token}"
