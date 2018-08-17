# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to exchange end points"""

from http import HTTPStatus
from jsonschema import validate
from pyswitcheo.internal.api import exchange
from pyswitcheo.utils import response_to_json, get_current_epoch_milli


def test_list_currency_pairs(url):
    """Test end points related to pairs."""

    response = exchange._list_currency_pairs(base_url=url.testnet, bases=["NEO"])

    json_response = response_to_json(response)
    schema = {
        "type": "array",
    }
    assert validate(json_response, schema) is None, "Failed to validate response from pairs end point"
    assert response.status_code == HTTPStatus.OK


def test_get_exchange_timestamp(url):
    """Test end points to fetch exchange timestamp."""

    response = exchange._get_exchange_timestamp(base_url=url.testnet)

    json_response = response_to_json(response)
    schema = {
        "type": "object",
    }
    assert validate(json_response, schema) is None, "Failed to validate response from get_exchange_timestamp end point"
    assert response.status_code == HTTPStatus.OK

    assert "timestamp" in json_response

    now = get_current_epoch_milli()
    assert abs(json_response["timestamp"] - now) <= 60, "Exchange timestamp is way off than current timestmap"


def test_list_contracts(url):
    """Test list contracts end points."""
    response = exchange._list_contracts(url.testnet)

    assert response.status_code == HTTPStatus.OK

    # Assuming NEO will always be in the deployed contracts.
    json_response = response_to_json(response)
    assert "NEO" in list(json_response.keys())


def test_get_contract_tokens(url):
    """Test listing of contract tokens with the deployed hash and their precision."""
    response = exchange._get_contract_tokens_info(url.testnet)

    assert response.status_code == HTTPStatus.OK

    # Assuming NEO will always be in the deployed contracts.
    json_response = response_to_json(response)
    assert "NEO" in list(json_response.keys())
    assert "GAS" in list(json_response.keys())
    assert "SWTH" in list(json_response.keys())

    assert "decimals" in json_response["NEO"]
    assert "decimals" in json_response["GAS"]
    assert "decimals" in json_response["SWTH"]

    assert json_response["GAS"]["decimals"] == 8, "Precision for GAS is different than in codebase"
    assert json_response["SWTH"]["decimals"] == 8, "Precision for SWTH is different than in codebase"
