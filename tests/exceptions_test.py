from collections import namedtuple

import pytest

from besepa.exceptions import MissingParam, Redirection, ResourceNotFound, UnauthorizedAccess


@pytest.fixture
def response_fixture():
    return namedtuple('Response', 'status_code reason')


class TestExceptions(object):

    def test_connection(self):
        error = ConnectionError({}, 'Test')
        assert str(error) == "Failed. Error message: Test"

    def test_redirect(self):
        error = Redirection({"Location": "http://example.com"})
        assert str(error) == "Failed. => http://example.com"

    def test_not_found(self, response_fixture):
        response = response_fixture(status_code="404", reason="Not Found")
        error = ResourceNotFound(response)
        assert str(error) == "Failed. Response status: %s. Response message: %s." % (
            response.status_code, response.reason)

    def test_unauthorized_access(self, response_fixture):
        response = response_fixture(status_code="401", reason="Unauthorized")
        error = UnauthorizedAccess(response)
        assert str(error) == "Failed. Response status: %s. Response message: %s." % (
            response.status_code, response.reason)

    def test_missing_param(self):
        error = MissingParam("Missing Payment Id")
        assert str(error) == "Missing Payment Id"

    def test_missing_config(self):
        error = MissingParam("Missing api_key")
        assert str(error) == "Missing api_key"
