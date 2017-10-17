try:  # pragma: no cover
    from unittest.mock import patch
except ImportError:  # pragma: no cover
    from mock import patch

import pytest

import besepa
from besepa.resource import Create, Delete, Find, List, Post, Resource, Update

besepa.configure(api_key='dummy')


class TestResource(object):
    def test_getter(self):
        data = {
            'name': 'testing',
            'amount': 10.0,
            'transaction': {'description': 'testing'},
            'items': [{'name': 'testing'}]
        }
        resource = Resource(data)
        assert resource.name == 'testing'
        assert resource['name'] == 'testing'
        assert resource.amount == 10.0
        assert resource.items[0].__class__ == Resource
        assert resource.items[0].name == 'testing'
        assert resource.items[0]['name'] == 'testing'
        assert resource.unknown is None
        with pytest.raises(KeyError):
            resource['unknown']

    def test_setter(self):
        data = {'name': 'testing'}
        resource = Resource(data)
        assert resource.name == 'testing'
        resource.name = 'changed'
        assert resource.name == 'changed'
        resource['name'] = 'again-changed'
        assert resource.name == 'again-changed'
        resource.transaction = {'description': 'testing'}
        assert resource.transaction.__class__ == Resource
        assert resource.transaction.description == 'testing'

    def test_to_dict(self):
        data = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": {
                        "type": "visa",
                        "number": "4417119669820331",
                        "expire_month": "11",
                        "expire_year": "2018",
                        "cvv2": "874",
                        "first_name": "Joe",
                        "last_name": "Shopper"
                    }
                }]
            }, "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "1.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                }, "amount": {
                    "total": "1.00",
                    "currency": "USD"
                }, "description": "This is the payment transaction description."
            }]
        }
        resource = Resource(data)
        assert resource.to_dict() == data

    def test_http_headers(self):
        data = {
            'name': 'testing',
            'header': {'My-Header': 'testing'}
        }
        resource = Resource(data)
        assert resource.header == {'My-Header': 'testing'}
        assert resource.http_headers() == {'My-Header': 'testing'}

    def test_passing_api(self):
        """
        Check that api objects are passed on to new resources when given
        """

        class DummyAPI(object):
            def post(self, *a, **k): pass

            def get(self, *a, **k): pass

        api = DummyAPI()

        # Conversion
        resource = Resource({'name': 'testing', }, api=api)
        assert resource.api == api
        convert_ret = resource.convert('test', {})
        assert convert_ret.api == api

        class TestResource(Find, List, Post):
            path = '/'

        # Find
        find = TestResource.find('resourceid', api=api)
        assert find.api == api

        # List
        list_ = TestResource.all(api=api)
        assert list_.api == api

        # Post
        post = TestResource({'id': 'id'}, api=api)
        post_ret = post.post('test')
        assert post_ret.api == api

    def test_default_resource(self):
        from besepa import api
        original = api.__api__

        class DummyAPI(object):
            def post(self, *a, **k): pass

            def get(self, *a, **k): pass

        # Make default api object a dummy api object
        default = api.__api__ = DummyAPI()

        resource = Resource({})
        assert resource.api == default

        class TestResource(Find, List, Post):
            path = '/'

        # Find
        find = TestResource.find('resourceid')
        assert find.api == default

        # List
        list_ = TestResource.all()
        assert list_.api == default

        api.__api__ = original  # Restore original api object

    def test_contains(self):
        resource = Resource({'name': 'testing'})
        assert True == ('name' in resource)
        assert False == ('testing' in resource)

    def test_representation(self):
        assert str(Resource({'name': 'testing'})) == str({'name': 'testing'})
        assert repr(Resource({'name': 'testing'})) == str({'name': 'testing'})

    def test_success(self):
        resource = Resource()
        assert resource.success() is True
        resource.error = 'Error'
        assert resource.success() is False


class TestCreate(object):
    @patch('resource_test.besepa.Api.post', autospec=True)
    def test_create(self, mock):
        class TestResource(Create):
            path = '/'

        attributes = {'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference': '1'}
        resource = TestResource(attributes)
        response = resource.create()

        mock.assert_called_once_with(resource.api, '/', {'testresource': attributes}, {})
        assert True is response


class TestList(object):
    @patch('resource_test.besepa.Api.get', autospec=True)
    def test_all(self, mock):
        class TestResource(List):
            path = '/'

        TestResource.convert_resources['response'] = TestResource
        mock.return_value = {
            'count': 1, 'response': [{'id': '1', 'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference': '1'}]}
        response = TestResource.all()

        mock.assert_called_once_with(response.api, '/')
        assert response.count == 1
        assert isinstance(response.response[0], TestResource)

    @patch('resource_test.besepa.Api.get', autospec=True)
    def test_all_return_list(self, mock):
        class TestResource(List):
            path = '/'

        mock.return_value = [{'id': '1', 'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference': '1'}]
        response = TestResource.all()

        mock.assert_called_once_with(response[0].api, '/')
        assert len(response) == 1
        assert isinstance(response[0], Resource)


class TestFind(object):
    @patch('resource_test.besepa.Api.get', autospec=True)
    def test_find(self, mock):
        class TestResource(Find):
            path = '/'

        test_resource = TestResource.find('1')

        mock.assert_called_once_with(test_resource.api, '/1')
        assert isinstance(test_resource, TestResource)


class TestUpdate(object):
    @patch('resource_test.besepa.Api.patch', autospec=True)
    def test_update(self, mock):
        class TestResource(Update):
            path = '/'

        updated_attributes = {'id': '1', 'name': 'Andrew Wiggin', 'taxid': '68571053A', 'reference': '1'}
        mock.return_value = updated_attributes
        test_resource = TestResource({'id': '1', 'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference': '1'})

        response = test_resource.update({'name': 'Andrew Wiggin'})

        mock.assert_called_once_with(test_resource.api, '/1', {'name': 'Andrew Wiggin'}, {})
        assert True is response
        assert test_resource.to_dict() == updated_attributes


class TestDelete(object):
    @patch('resource_test.besepa.Api.delete', autospec=True)
    def test_delete(self, mock):
        class TestResource(Delete):
            path = '/'

        test_resource = TestResource({'id': '1', 'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference': '1'})
        response = test_resource.delete()

        mock.assert_called_once_with(test_resource.api, '/1')
        assert True is response


class TestPost(object):
    @patch('resource_test.besepa.Api.post', autospec=True)
    def test_post(self, mock):
        class TestResource(Post):
            path = '/'

            def test(self, attributes):
                return self.post('test', attributes, self)

        attributes = {'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference': '1'}
        resource = TestResource({'id': '1'})
        response = resource.test(attributes)

        mock.assert_called_once_with(resource.api, '/1/test', attributes, {})
        assert True is response
