import besepa.util as util
from besepa.api import default as default_api


class Resource(object):
    """Base class for all REST services
    """
    convert_resources = {}

    def __init__(self, attributes=None, api=None):
        attributes = attributes or {}
        self.__dict__['api'] = api or default_api()

        super(Resource, self).__setattr__('__data__', {})
        super(Resource, self).__setattr__('error', None)
        super(Resource, self).__setattr__('headers', {})
        super(Resource, self).__setattr__('header', {})
        self.merge(attributes)

    def http_headers(self):
        """Generate HTTP header
        """
        return util.merge_dict(self.header, self.headers)

    def __str__(self):
        return self.__data__.__str__()

    def __repr__(self):
        return self.__data__.__str__()

    def __getattr__(self, name):
        return self.__data__.get(name)

    def __setattr__(self, name, value):
        try:
            # Handle attributes(error, header)
            super(Resource, self).__getattribute__(name)
            super(Resource, self).__setattr__(name, value)
        except AttributeError:
            self.__data__[name] = self.convert(name, value)

    def __contains__(self, item):
        return item in self.__data__

    def success(self):
        return self.error is None

    def merge(self, new_attributes):
        """Merge new attributes e.g. response from a post to Resource
        """
        for k, v in new_attributes.items():
            setattr(self, k, v)

    def convert(self, name, value):
        """Convert the attribute values to configured class
        """
        if isinstance(value, dict):
            cls = self.convert_resources.get(name, Resource)
            return cls(value, api=self.api)
        elif isinstance(value, list):
            new_list = []
            for obj in value:
                new_list.append(self.convert(name, obj))
            return new_list
        else:
            return value

    def __getitem__(self, key):
        return self.__data__[key]

    def __setitem__(self, key, value):
        self.__data__[key] = self.convert(key, value)

    def to_dict(self):

        def parse_object(value):
            if isinstance(value, Resource):
                return value.to_dict()
            elif isinstance(value, list):
                return list(map(parse_object, value))
            else:
                return value

        return dict((key, parse_object(value)) for (key, value) in self.__data__.items())


class Find(Resource):

    @classmethod
    def find(cls, resource_id, api=None):
        """Locate resource e.g. customer with given id

        Usage::
            >>> payment = Customer.find("1")
        """
        api = api or default_api()

        url = util.join_url(cls.path, str(resource_id))
        return cls(api.get(url), api=api)


class List(Resource):

    list_class = Resource

    @classmethod
    def all(cls, params=None, api=None):
        """Get list of resources

        Usage::

            >>> payment_histroy = Customer.all({'per_page': 2})
        """
        api = api or default_api()
        url = cls.path if params is None else util.join_url_params(cls.path, params)

        try:
            response = api.get(url)
            return cls.list_class(response, api=api)
        except AttributeError:
            # To handle the case when response is JSON Array
            if isinstance(response, list):
                new_resp = [cls.list_class(elem, api=api) for elem in response]
                return new_resp


class Create(Resource):

    def create(self):
        """Creates a resource e.g. payment

        Usage::

            >>> customer = Customer({})
            >>> customer.create() # return True or False
        """
        resource_name = self.__class__.__name__.lower()
        payload = {resource_name: self.to_dict()}
        new_attributes = self.api.post(self.path, payload, self.http_headers())
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Update(Resource):
    """Partial update or modify resource

    Usage::

        >>> customer.update([{'name': 'Andrew'}])
    """

    def update(self, attributes=None):
        attributes = attributes or self.to_dict()
        url = util.join_url(self.path, str(self['id']))
        new_attributes = self.api.patch(url, attributes, self.http_headers())
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Delete(Resource):

    def delete(self):
        """Deletes a resource e.g. bank_account

        Usage::

            >>> bank_account.delete()
        """
        url = util.join_url(self.path, str(self['id']))
        new_attributes = self.api.delete(url)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Post(Resource):

    def post(self, name, attributes=None, cls=Resource, fieldname='id'):
        """Constructs url with passed in headers and makes post request via
        post method in api class.

        Usage::

            >>> client.post("stats", {'id': '1234'}, client)  # return True or False
        """
        attributes = attributes or {}
        url = util.join_url(self.path, str(self[fieldname]), name)
        if not isinstance(attributes, Resource):
            attributes = Resource(attributes, api=self.api)
        new_attributes = self.api.post(url, attributes.to_dict(), attributes.http_headers())
        if isinstance(cls, Resource):
            cls.error = None
            cls.merge(new_attributes)
            return self.success()
        else:
            return cls(new_attributes, api=self.api)
