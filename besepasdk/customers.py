from besepasdk.resource import Create, Delete, Find, List, Update


class Customer(List, Find, Create, Delete, Update):
    """Customer class wrapping the REST api/1/customers endpoint

    Usage::

        >>> customers = Customer.all()

        >>> customer = Customer.new({})
        >>> customer.create()  # return True or False
    """
    path = "api/1/customers"


Customer.convert_resources['response'] = Customer
