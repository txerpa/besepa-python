import datetime
import json
import logging
import os
import platform
import ssl

import requests

from besepa import __version__, exceptions, util
from besepa.config import __endpoint_map__

log = logging.getLogger(__name__)


class Api(object):
    # User-Agent for HTTP request
    ssl_version = ssl.OPENSSL_VERSION
    library_details = "requests %s; python %s; %s" % (requests.__version__, platform.python_version(), ssl_version)
    user_agent = "BesepaSDK/Besepa-Python-SDK %s (%s)" % (__version__, library_details)

    def __init__(self, options=None, **kwargs):
        """Create API object

        Usage::

            >>> import besepa
            >>> api = besepa.Api(mode="sandbox", api_key='API_KEY')
        """
        kwargs = util.merge_dict(options or {}, kwargs)

        self.mode = kwargs.get("mode", "sandbox")

        if self.mode not in ("live", "sandbox"):
            raise exceptions.InvalidConfig("Configuration Mode Invalid", "Received: %s" % self.mode,
                                           "Required: live or sandbox")

        self.endpoint = self.default_endpoint()
        # Mandatory parameter, so not using `dict.get`
        self.api_key = kwargs["api_key"]
        self.proxies = kwargs.get("proxies", None)

        self.options = kwargs

    def default_endpoint(self):
        return __endpoint_map__.get(self.mode)

    def request(self, url, method, body=None, headers=None):
        """Make HTTP call, formats response and does error handling. Uses http_call method in API class.

        Usage::

            >>> api.request("https://sandbox.besepa.com/api/1/customers", "GET", {})
            >>> api.request("https://sandbox.besepa.com/api/1/customers", "POST",
             "{'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference: C1'}", {} )
        """
        http_headers = util.merge_dict(self.headers(), headers or {})

        try:
            return self.http_call(url, method, json=body, headers=http_headers)
        # Format Error message for bad request
        except exceptions.BadRequest as error:
            return {"error": json.loads(error.content)}

    def http_call(self, url, method, **kwargs):
        """Makes a http call. Logs response information.
        """
        log.info('Request[%s]: %s' % (method, url))

        if self.mode.lower() != 'live':
            request_headers = kwargs.get("headers", {})
            request_body = kwargs.get("json", {})
            log.debug("Level: " + self.mode)
            log.debug('Request: \nHeaders: %s\nBody: %s' % (str(request_headers), str(request_body)))
        else:  # pragma: no cover
            log.info('Not logging full request/response headers and body in live mode for compliance')

        start_time = datetime.datetime.now()
        response = requests.request(method, url, proxies=self.proxies, **kwargs)
        duration = datetime.datetime.now() - start_time
        log.info('Response[%d]: %s, Duration: %s.%ss.' % (
            response.status_code, response.reason, duration.seconds, duration.microseconds))

        debug_id = response.headers.get('Besepa-Debug-Id')
        if debug_id:  # pragma: no cover
            log.debug('debug_id: %s' % debug_id)
        if self.mode.lower() != 'live':  # pragma: no cover
            log.debug('Headers: %s\nBody: %s' % (str(response.headers), response.content.decode('utf-8')))

        return self.handle_response(response, response.content.decode('utf-8'))

    @staticmethod
    def handle_response(response, content):
        """Validate HTTP response
        """
        status = response.status_code
        if status in (301, 302, 303, 307):
            raise exceptions.Redirection(response, content)
        elif 200 <= status <= 299:
            return json.loads(content).get('response') if content else {}
        elif status == 400:
            raise exceptions.BadRequest(response, content)
        elif status == 401:
            raise exceptions.UnauthorizedAccess(response, content)
        elif status == 403:
            raise exceptions.ForbiddenAccess(response, content)
        elif status == 404:
            raise exceptions.ResourceNotFound(response, content)
        elif status == 405:
            raise exceptions.MethodNotAllowed(response, content)
        elif status == 409:
            raise exceptions.ResourceConflict(response, content)
        elif status == 410:
            raise exceptions.ResourceGone(response, content)
        elif status == 422:
            raise exceptions.ResourceInvalid(response, content)
        elif 401 <= status <= 499:
            raise exceptions.ClientError(response, content)
        elif 500 <= status <= 599:
            raise exceptions.ServerError(response, content)
        else:
            raise exceptions.ConnectionError(response, content, "Unknown response code: #{response.code}")

    def headers(self):
        """Default HTTP headers
        """
        return {
            "Authorization": ("Bearer %s" % self.api_key),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent
        }

    def get(self, action, headers=None):
        """Make GET request

        Usage::

            >>> api.get("api/1/customers")
            >>> api.get("api/1/customers/1")
        """
        return self.request(util.join_url(self.endpoint, action), 'GET', headers=headers or {})

    def post(self, action, params=None, headers=None):
        """Make POST request

        Usage::

            >>> api.post("api/1/customers", {'name': 'Ender Wiggin', 'taxid': '68571053A', 'reference: C1'})
        """
        return self.request(util.join_url(self.endpoint, action), 'POST', body=params or {}, headers=headers or {})

    def patch(self, action, params=None, headers=None):
        """Make PATCH request

        Usage::

            >>> api.patch("api/1/customers/1", {'name': 'Andrew Wiggins'})
        """
        return self.request(util.join_url(self.endpoint, action), 'PATCH', body=params or {}, headers=headers or {})

    def delete(self, action, headers=None):
        """Make DELETE request
        """
        return self.request(util.join_url(self.endpoint, action), 'DELETE', headers=headers or {})


__api__ = None


def default():
    """Returns default api object and if not present creates a new one
    By default points to developer sandbox
    """
    global __api__
    if __api__ is None:
        try:
            api_key = os.environ["BESEPA_API_KEY"]
        except KeyError:
            raise exceptions.MissingConfig("Required BESEPA_API_KEY. \
                Refer http://docs.besepaen.apiary.io/#introduction/authorization")

        __api__ = Api(mode=os.environ.get("BESEPA_MODE", "sandbox"), api_key=api_key)
    return __api__


def set_config(options=None, **config):
    """Create new default api object with given configuration
    """
    global __api__
    __api__ = Api(options or {}, **config)
    return __api__


configure = set_config
