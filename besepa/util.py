
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
    to_rstrip = [url] + list(paths[:-1])
    parts = [path.rstrip('/') for path in to_rstrip] + [paths[-1]]
    return "/".join(path.lstrip('/') for path in parts)


def join_url_params(url, params):
    """Constructs percent-encoded query string from given parms dictionary
     and appends to given url
    Usage::
        >>> util.join_url_params("example.com/index.html", {"page-id": 2, "Company": "Tx Erpa"})
        example.com/index.html?page-id=2&Company=Tx+Erpa
    """
    return url + "?" + urlencode(params)


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
