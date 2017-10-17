from besepa import util
from besepa.resource import Create, Delete, Find, List, Update, Post, Resource


class Customer(List, Find, Create, Delete, Update, Post):
    """Customer class wrapping the REST api/1/customers endpoint

    Usage::

        >>> customers = Customer.all()

        >>> customer = Customer.new({})
        >>> customer.create()  # return True or False
    """
    path = "api/1/customers"

    def create_bank_account(self, attributes):
        # /customers/invoices/<CUSTOMER-ID>/bank_accounts
        return self.post('bank_accounts', attributes)

    def list_bank_accounts(self):
        # /customers/invoices/<CUSTOMER-ID>/bank_accounts
        endpoint = util.join_url(self.path, str(self['id']), 'bank_accounts')
        response = self.api.get(endpoint)
        try:
            return Resource(response, api=self.api)
        except AttributeError:
            # To handle the case when response is JSON Array
            if isinstance(response, list):
                new_resp = [Resource(elem, api=self.api) for elem in response]
                return new_resp


Customer.convert_resources['bank_accounts'] = Resource
Customer.convert_resources['bank_account'] = Resource
Customer.convert_resources['mandate'] = Resource
