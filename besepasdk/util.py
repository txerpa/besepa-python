import re

try:  # pragma: no cover
    from urllib.parse import urlencode
except ImportError:  # pragma: no cover
    from urllib import urlencode


def join_url(url, *paths):
    """
    Joins individual URL strings together, and returns a single string.

    Usage::

        >>> util.join_url("example.com", "index.html")
        'example.com/index.html'
    """
    for path in paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url


def merge_dict(data, *override):
    """
    Merges any number of dictionaries together, and returns a single dictionary

    Usage::

        >>> util.merge_dict({"foo": "bar"}, {1: 2}, {"Tx": "erpa"})
        {1: 2, 'foo': 'bar', 'Tx': 'erpa'}
    """
    result = {}
    for current_dict in (data,) + override:
        result.update(current_dict)
    return result