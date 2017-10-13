try:  # pragma: no cover
    from unittest.mock import patch
except ImportError:  # pragma: no cover
    from mock import patch
import besepasdk as besepa


besepa.configure(api_key='dummy')


class TestResource(object):

    @patch('customers_test.besepa.Api.get', autospec=True)
    def test_path(self, mock):
        customers = besepa.Customer.all()

        mock.assert_called_once_with(customers.api, 'api/1/customers')
