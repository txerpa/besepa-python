import pytest

from besepasdk import util


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

    @pytest.mark.parametrize('expected, data, override', [
        ({1: 2, 'foo': 'bar', 'Tx': 'erpa'}, {"foo": "bar"}, ({1: 2}, {"Tx": "erpa"})),
    ])
    def test_merge_dict(self, expected, data, override):
        result = util.merge_dict(data, *override)
        assert result == expected
