# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to orders end points"""

from http import HTTPStatus
from jsonschema import validate
from pyswitcheo.internal.api import orders
from pyswitcheo.utils import response_to_json
from pyswitcheo.schemas import CREATE_ORDER_RESPONSE_SCHEMA


def test_list_orders(url):
    """Test listing of orders."""
    contract_hash = "a195c1549e7da61b8da315765a790ac7e7633b82"
    # encrypted_key = b"6PYKozqwKwRYi77GN3AwTwXEssJZWbfneYKEYbiSeuNtVTGPFT2Q7EJpjY"
    pub_key = "ANVLCD3xqGXKhDnrivpVFvDLcvkpgPbbMt"
    # priv_key_wif = "L2vHHz8L4rtkUkFaxzQoPro33bo7McYMRoUU69DjE334a8NT8zc9"

    orders_response = orders._list_orders(base_url=url.testnet, address=pub_key, contract_hash=contract_hash)
    json_response = response_to_json(orders_response)
    assert orders_response.status_code == HTTPStatus.OK

    # json response comes out to be a list [{},{}]
    assert len(json_response[0].keys()) > 0


def test_create_and_execute_orders(url):
    """Test creation and execution of orders."""
    contract_hash = "a195c1549e7da61b8da315765a790ac7e7633b82"

    # address = "AG9YqjpmoQC5Ufxo2JUr8zCSrXba9krc7g"
    priv_key_wif = "L4FSnRosoUv22cCu5z7VEEGd2uQWTK7Me83vZxgQQEsJZ2MReHbu"
    orders_response = orders._create_order(base_url=url.testnet, priv_key_wif=priv_key_wif, pair="SWTH_NEO",
                                           blockchain="neo", side="sell", price=0.1, want_amount=0.5, asset_id="SWTH",
                                           use_native_tokens=True, order_type="limit", contract_hash=contract_hash)

    orders_json_resp = response_to_json(orders_response)
    assert validate(orders_json_resp, CREATE_ORDER_RESPONSE_SCHEMA) is None, ("Failed to validate response"
                                                                              "from create orders")
    assert orders_response.status_code == HTTPStatus.OK

    execute_response = orders._execute_order(base_url=url.testnet,
                                             order=orders_json_resp,
                                             priv_key_wif=priv_key_wif,)
    assert execute_response.status_code == HTTPStatus.OK
