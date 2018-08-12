# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to offers end points"""

import pytest
from http import HTTPStatus
from jsonschema import validate
from pyswitcheo.internal.api import offers
from pyswitcheo.utils import response_to_json


@pytest.mark.parametrize("blockchain, pair, contract_hash, error_msg", [
    ("NEO", "SWTH_NEO", "eed0d2e14b0027f5f30ade45f2b23dc57dd54ad2", "list offers with base NEO should not fail."),
    ("neo", "SWTH_NEO", "eed0d2e14b0027f5f30ade45f2b23dc57dd54ad2", "list offers with base NEO should not fail."),
])
def test_list_offers(blockchain, pair, contract_hash, error_msg, url):
    """Get offers for the resources."""

    response = offers._list_offers(base_url=url.testnet, blockchain=blockchain, pair=pair, contract_hash=contract_hash)

    json_response = response_to_json(response)
    schema = {
        "type": "array",
        "properties": {
            "price": {"type": "number"},
            "name": {"type": "string"},
        },
    }
    assert validate(json_response, schema) is None, "Failed to validate response from List offers"
    assert response.status_code == HTTPStatus.OK, error_msg
