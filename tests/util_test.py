import pytest

from besepa import util


class TestUtil(object):
    @pytest.mark.parametrize('left, right, expected', [
        ('payment', '1', 'payment/1'),
        ('payment/', '1', 'payment/1'),
        ('payment', '/1', 'payment/1'),
        ('payment/', '/1', 'payment/1'),
    ])
    def test_join_url(self, left, right, expected):
        url = util.join_url(left, right)
        assert url == expected

    def test_join_url_params(self):
        single_param_url = util.join_url_params('customers', {'per_page': 1})
        multiple_params_url = util.join_url_params('customers', {'per_page': 1, 'group_id': 4321})
        assert single_param_url == 'customers?per_page=1'
        assert multiple_params_url in ('customers?group_id=4321&per_page=1', 'customers?per_page=1&group_id=4321')

    @pytest.mark.parametrize('expected, data, override', [
        ({1: 2, 'foo': 'bar', 'Tx': 'erpa'}, {'foo': 'bar'}, ({1: 2}, {'Tx': 'erpa'})),
    ])
    def test_merge_dict(self, expected, data, override):
        result = util.merge_dict(data, *override)
        assert result == expected
