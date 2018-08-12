# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Custom exception raised by pyswitcheo"""

# Human readable http error codes
import json
from http import HTTPStatus

_ERR = {
    HTTPStatus.BAD_REQUEST: "Your request is badly formed.",
    HTTPStatus.UNAUTHORIZED: "You did not provide a valid signature.",
    HTTPStatus.NOT_FOUND: "The specified endpoint or resource could not be found.",
    HTTPStatus.NOT_ACCEPTABLE: "You requested a format that isn't json.",
    HTTPStatus.TOO_MANY_REQUESTS: "Slow down requests and use Exponential backoff timing.",
    HTTPStatus.UNPROCESSABLE_ENTITY: "Your request had validation errors.",
    HTTPStatus.INTERNAL_SERVER_ERROR: "We had a problem with our server. Try again later.",
    HTTPStatus.SERVICE_UNAVAILABLE: "We're temporarily offline for maintenance. Please try again later.",
}


class HTTPResponseError(Exception):
    """Wrapper around Exception to raise custom messages."""

    def __init__(self, response):
        self.value = {
            "code": response.status_code,
            "server_msg": response.text,
            "err_msg": _ERR.get(response.status_code, "Unexpected error"),
        }

    def __str__(self):
        return json.dumps(self.value, indent=4, sort_keys=True)
