# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to deposits end points"""

from http import HTTPStatus
from jsonschema import validate
from pyswitcheo.internal.api import deposits
from pyswitcheo.utils import response_to_json
from pyswitcheo.schemas import CREATE_DEPOSIT_SCHEMA


def test_create_deposit(url):
    """Test creation of deposits."""

    # encrypted_key = b"6PYKozqwKwRYi77GN3AwTwXEssJZWbfneYKEYbiSeuNtVTGPFT2Q7EJpjY"
    # pub_key = "ANVLCD3xqGXKhDnrivpVFvDLcvkpgPbbMt"
    priv_key_wif = "L2vHHz8L4rtkUkFaxzQoPro33bo7McYMRoUU69DjE334a8NT8zc9"

    deposit_response = deposits._create_deposit(base_url=url.testnet, asset_id="SWTH", amount=10,
                                                contract_hash="a195c1549e7da61b8da315765a790ac7e7633b82",
                                                priv_key_wif=priv_key_wif, blockchain="neo")
    json_response = response_to_json(deposit_response)
    assert validate(json_response, CREATE_DEPOSIT_SCHEMA) is None, "Failed to validate response from deposit offers"
    assert deposit_response.status_code == HTTPStatus.OK


def test_create_and_execute_deposit(url):
    """Test creation and execution of deposits."""

    # encrypted_key = b"6PYKozqwKwRYi77GN3AwTwXEssJZWbfneYKEYbiSeuNtVTGPFT2Q7EJpjY"
    # pub_key = "ANVLCD3xqGXKhDnrivpVFvDLcvkpgPbbMt"
    priv_key_wif = "L2vHHz8L4rtkUkFaxzQoPro33bo7McYMRoUU69DjE334a8NT8zc9"

    deposit_response = deposits._create_deposit(base_url=url.testnet, asset_id="SWTH", amount=10,
                                                contract_hash="a195c1549e7da61b8da315765a790ac7e7633b82",
                                                priv_key_wif=priv_key_wif, blockchain="neo")
    deposit_json_resp = response_to_json(deposit_response)
    assert validate(deposit_json_resp, CREATE_DEPOSIT_SCHEMA) is None, "Failed to validate resp from deposit offers"
    assert deposit_response.status_code == HTTPStatus.OK

    execute_response = deposits._execute_deposit(base_url=url.testnet,
                                                 deposit=deposit_json_resp,
                                                 priv_key_wif=priv_key_wif,)
    assert execute_response.status_code == HTTPStatus.OK
