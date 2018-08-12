# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to pairs end points"""

from http import HTTPStatus
from jsonschema import validate
from pyswitcheo.internal.api import pairs
from pyswitcheo.utils import response_to_json


def test_list_currency_pairs(url):
    """Test end points related to pairs."""

    response = pairs._list_currency_pairs(base_url=url.testnet, bases=["NEO"])

    json_response = response_to_json(response)
    schema = {
        "type": "array",
    }
    assert validate(json_response, schema) is None, "Failed to validate response from pairs end point"
    assert response.status_code == HTTPStatus.OK
