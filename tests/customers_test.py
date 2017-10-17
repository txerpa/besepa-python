try:  # pragma: no cover
    from unittest.mock import patch
except ImportError:  # pragma: no cover
    from mock import patch
import besepa
from besepa.resource import Resource

besepa.configure(api_key='dummy')


class TestResource(object):

    @patch('customers_test.besepa.Api.get', autospec=True)
    def test_path(self, mock):
        customers = besepa.Customer.all()

        mock.assert_called_once_with(customers.api, 'api/1/customers')

    @patch('customers_test.besepa.Api.post', autospec=True)
    def test_create_bank_account(self, mock):
        customer = besepa.Customer({'id': '1'})
        response = customer.create_bank_account({'iban': 'NL33ABNA0618708937'})

        mock.assert_called_once_with(
            customer.api, 'api/1/customers/1/bank_accounts', {'iban': 'NL33ABNA0618708937'}, {})
        assert response.error is None

    @patch('customers_test.besepa.Api.get', autospec=True)
    def test_list_bank_accounts(self, mock):
        customer = besepa.Customer({'id': '1'})
        mock.return_value = [{'id': '1', 'iban': 'NL33ABNA0618708937'}]
        response = customer.list_bank_accounts()

        mock.assert_called_once_with(response[0].api, 'api/1/customers/1/bank_accounts')
        assert len(response) == 1
        assert isinstance(response[0], Resource)
