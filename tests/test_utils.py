# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to test utils functions."""

import pytest
from http import HTTPStatus
from pyswitcheo.internal.urls import balances
from pyswitcheo.utils import format_urls, response_else_exception, jsonify


@pytest.mark.parametrize("base_url, test_end_point, expected", [
    ("https://api.switcheo.network/v2", balances.LIST_BALANCES, "https://api.switcheo.network/v2/balances"),
    ("https://test-api.switcheo.network/v2", balances.LIST_BALANCES, "https://test-api.switcheo.network/v2/balances"),
])
def test_format_urls(base_url, test_end_point, expected):
    """Formatting urls test."""
    actual = format_urls(base_url, test_end_point)
    assert expected == actual


def __create_fake_responses(code):
    """Create fake response to test."""
    from requests.models import Response
    response = Response()
    response.code = "blah"
    response.error_type = "blah"
    response.status_code = code
    return response


@pytest.mark.parametrize("response", [
    (__create_fake_responses(HTTPStatus.BAD_REQUEST)),
    (__create_fake_responses(HTTPStatus.UNAUTHORIZED)),
])
def test_response_else_exception(response):
    """Tests for exception in case response is different than 200."""
    with pytest.raises(Exception) as excinfo:
        response_else_exception(response)
    assert "server_msg" in str(excinfo.value)
    assert "err_msg" in str(excinfo.value)
    assert "code" in str(excinfo.value)


@pytest.mark.parametrize("json_object, want", [
    ({"a": "aa", "b": "bb"}, '{"a":"aa","b":"bb"}')
])
def test_jsonify(json_object, want):
    """Tests for jsonify function."""
    got = jsonify(json_object)
    assert got == want
