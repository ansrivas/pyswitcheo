# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example to interact with orders."""

from pyswitcheo.api import SwitcheoApi
from pyswitcheo.utils import response_to_json


def list_order(client, address, contract_hash):
    """List order example."""

    response = client.list_orders(address=address, contract_hash=contract_hash, pair="SWTH_NEO")
    orders = response_to_json(response)

    # for eg. print only orders which were of type sell
    # check the schema `schemas.CREATE_ORDER_RESPONSE_SCHEMA` (from pyswitcheo import schemas)
    for order in orders:
        if order["side"] == 'sell':
            print(order)


if __name__ == '__main__':
    client = SwitcheoApi(base_url="https://test-api.switcheo.network")

    contract_hash = 'a195c1549e7da61b8da315765a790ac7e7633b82'
    priv_key_wif = 'L4FSnRosoUv22cCu5z7VEEGd2uQWTK7Me83vZxgQQEsJZ2MReHbu'
    address = "AG9YqjpmoQC5Ufxo2JUr8zCSrXba9krc7g"

    # Use this example for listing orders
    # list_order(client, address, contract_hash)

    # Following can be used to create orders
    create_order_resp = client.create_order(priv_key_wif=priv_key_wif, pair="SWTH_NEO",
                                            blockchain="neo", side="sell", price=0.01, want_amount=0.05,
                                            use_native_tokens=True, order_type="limit", contract_hash=contract_hash)

    order_object = response_to_json(create_order_resp)

    # This order object then can be used to cancel orders
    # client.create_cancellation(order_id=order_object["id"], priv_key_wif=priv_key_wif)
