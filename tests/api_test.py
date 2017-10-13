import os
from collections import namedtuple

import pytest

import besepasdk as besepa

try:  # pragma: no cover
    from unittest.mock import Mock, patch
except ImportError:  # pragma: no cover
    from mock import Mock, patch


@pytest.fixture
def api():
    import besepasdk
    return besepasdk.Api(api_key='dummy')


@pytest.fixture
def request_mock(api):
    api.request = Mock()
    return api


@pytest.fixture
def http_call_mock(api):
    api.http_call = Mock()
    return api


class TestApi(object):

    @pytest.mark.parametrize('mode, expected_enpoint', [
        ('live', 'https://api.besepa.com'), ('sandbox', 'https://sandbox.besepa.com')
    ])
    def test_endpoint(self, mode, expected_enpoint):
        new_api = besepa.Api(mode=mode, api_key='dummy')

        assert new_api.endpoint == expected_enpoint

    def test_bad_mode(self):
        with pytest.raises(besepa.exceptions.InvalidConfig):
            besepa.Api(mode='bad', api_key='dummy')

    @patch('besepasdk.api.requests.request', return_value=Mock)
    def test_http_call(self, requests_mock, api):
        Response = namedtuple('Response', 'status_code reason headers content')
        requests_mock.return_value = Response(200, 'Failed', {}, 'Test'.encode())
        api.handle_response = Mock()
        api.http_call('https://sandbox.besepa.com/api/1/customers', 'GET')
        requests_mock.assert_called_once_with('GET', 'https://sandbox.besepa.com/api/1/customers', proxies=None)
        api.handle_response.assert_called_once_with(requests_mock.return_value, 'Test')

    def test_bad_request(self, http_call_mock):
        http_call_mock.http_call.side_effect = besepa.exceptions.BadRequest('error', '""')

        customer = http_call_mock.request('https://sandbox.besepa.com/api/1/customers', 'GET')

        http_call_mock.http_call.assert_called_once_with(
            'https://sandbox.besepa.com/api/1/customers', 'GET', data='null', headers=http_call_mock.headers())
        assert customer.get('error') is not None

    def test_get(self, request_mock):
        request_mock.get('api/1/customers?page=1')

        request_mock.request.assert_called_once_with(
            'https://sandbox.besepa.com/api/1/customers?page=1', 'GET', headers={})

    def test_post(self, request_mock):
        request_mock.request.return_value = {'id': 'test'}
        customer_attributes = {'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference': '1'}

        customer = request_mock.post('api/1/customers', customer_attributes)

        request_mock.request.assert_called_once_with(
            'https://sandbox.besepa.com/api/1/customers', 'POST', body=customer_attributes, headers={})
        assert customer.get('error') is None
        assert customer.get('id') is not None

    def test_patch(self, request_mock):
        request_mock.request.return_value = {'id': 'test'}
        customer_attributes = {'name': 'Andrew Wiggin'}

        customer = request_mock.patch('api/1/customers/1', customer_attributes)

        request_mock.request.assert_called_once_with(
            'https://sandbox.besepa.com/api/1/customers/1', 'PATCH', body=customer_attributes, headers={})
        assert customer.get('error') is None
        assert customer.get('id') is not None

    def test_delete(self, request_mock):
        request_mock.delete('api/1/customers/1')

        request_mock.request.assert_called_once_with(
            'https://sandbox.besepa.com/api/1/customers/1', 'DELETE', headers={})

    def test_not_found(self, request_mock):
        request_mock.request.side_effect = besepa.ResourceNotFound('error')

        with pytest.raises(besepa.ResourceNotFound):
            request_mock.get('api/1/customers/2')

    def test_hanlde_response(self, api):
        response = Mock()
        response.status_code = 200
        assert api.handle_response(response, '""') == ""
        assert api.handle_response(response, None) == {}

    @pytest.mark.parametrize('code, expected_exception', [
        (301, besepa.exceptions.Redirection),
        (302, besepa.exceptions.Redirection),
        (400, besepa.exceptions.BadRequest),
        (401, besepa.exceptions.UnauthorizedAccess),
        (403, besepa.exceptions.ForbiddenAccess),
        (404, besepa.exceptions.ResourceNotFound),
        (405, besepa.exceptions.MethodNotAllowed),
        (409, besepa.exceptions.ResourceConflict),
        (410, besepa.exceptions.ResourceGone),
        (422, besepa.exceptions.ResourceInvalid),
        (402, besepa.exceptions.ClientError),
        (500, besepa.exceptions.ServerError),
        (600, besepa.exceptions.ConnectionError),
    ])
    def test_hanlde_response_exception(self, code, expected_exception, api):
        response = Mock()
        response.status_code = code
        with pytest.raises(expected_exception):
            api.handle_response(response, None)


def test_default_configuration():
    default = besepa.api.__api__
    besepa.api.__api__ = None
    os.environ["BESEPA_API_KEY"] = "EBWKjlELKMYqRNQ6sYvFo64FtaRLRR5BdHEESmha49TM"

    assert isinstance(besepa.api.default(), besepa.Api)
    assert besepa.api.default().mode == "sandbox"
    assert besepa.api.default().api_key == "EBWKjlELKMYqRNQ6sYvFo64FtaRLRR5BdHEESmha49TM"

    del os.environ["BESEPA_API_KEY"]
    besepa.api.__api__ = default


def test_default_configuration_missing_api_key():
    default = besepa.api.__api__
    besepa.api.__api__ = None
    with pytest.raises(besepa.exceptions.MissingConfig):
        besepa.api.default()
    besepa.api.__api__ = default
