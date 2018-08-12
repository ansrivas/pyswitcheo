# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Orders are instructions to buy or sell assets on Switcheo Exchange.
At the moment, only Limit orders are available. Market, Fill-Or-Cancel, Make-Or-Cancel, etc. strategies are not
available yet.
As such, orders will contain a combination of zero or one make and/or zero or more fills.
Once an order is placed, the funds required for the order is removed from the user's balance and placed on hold
until the order is filled or the order is cancelled.
"""

import logging
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls import orders
from pyswitcheo.datatypes.fixed8 import Fixed8
from pyswitcheo.serialization import sign_msg, sign_array, sign_transaction
from pyswitcheo.crypto_utils import (
    encode_msg,
    get_script_hash_from_address,
    get_private_key_from_wif,
    get_public_key_script_hash_from_wif,
)

logger = logging.getLogger(__name__)


def _list_orders(base_url, address, contract_hash, pair=None):
    """Retrieves the best 70 offers (per side) on the offer book.

    Args:
        base_url (str)     : This paramter governs whether to connect to test or mainnet.
        address (str)      : Only returns orders made by this address.
        contract_hash (str): Only return offers for the contract hash. e.g. eed0d2e14b0023dc57dd54ad2
        pair (str)         : The pair to buy or sell on. (optional)

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response:
        [
          {
            "id": "c415f943-bea8-4dbf-82e3-8460c559d8b7",
            "blockchain": "neo",
            "contract_hash": "c41d8b0c30252ce7e8b6d95e9ce13fdd68d2a5a8",
            "address": "20abeefe84e4059f6681bf96d5dcb5ddeffcc377",
            "side": "buy",
            "offer_asset_id": "c56f33fc6ecfcd0c225c4ab356fee0faebe74a6daff7c9b",
            "want_asset_id": "602c79718b16e442de58778e148d0bb16cee7969282de7",
            "offer_amount": "100000000",
            "want_amount": "20000000",
            "transfer_amount": "0",
            "priority_gas_amount": "0",
            "use_native_token": false,
            "native_fee_transfer_amount": 0,
            "deposit_txn": null,
            "created_at": "2018-05-15T10:54:20.054Z",
            "status": "processed",
            "fills": [...],
            "makes": [...]
          }
        ]
    """
    address = get_script_hash_from_address(address)
    params = {"address": address, "contract_hash": contract_hash}

    if pair:
        params["pair"] = pair
    url = utils.format_urls(base_url, orders.LIST_ORDERS)
    resp = requests.get(url, params=params)
    return utils.response_else_exception(resp)


def _create_order(
    base_url,
    priv_key_wif,
    pair,
    blockchain,
    side,
    price,
    want_amount,
    use_native_tokens,
    order_type,
    contract_hash,
):
    """This endpoint creates an order which can be executed through Broadcast Order.

    Orders can only be created after sufficient funds have been deposited into the user's contract
    balance. A successful order will have zero or one make and/or zero or more fills.

    NOTE: Based on the params you are using, let's say you are trying to sell SWTH for NEO at the price of 0.01
    exchange rate. The `want_amount` for a sell would be the amount of NEO you want. For eg
    we want_amount of neo = 0.1 and we want to sell 1 SWTH for 0.0005 NEOs. In this case the sell order would become
    at 0.0005 exchange rate for 0.1 NEO and 200 SWTH ( so you need to have 200 SWTH in your smart-contract)

    IMPORTANT: After calling this endpoint, the Broadcast Order endpoint has to be called for the order to be executed.

    Args:
        base_url (str)           : This paramter governs whether to connect to test or mainnet.
        priv_key_wif (str)       : The private key wif of the user.
        pair (str)               : The pair to buy or sell on.
        blockchain (str)         : Blockchain that the pair is on. Possible values are: neo.
        address (str)            : Address of the order maker. Do not include this in the parameters to be signed.
        side (str)               : Whether to buy or sell on this pair. Possible values are: buy, sell.
        price (str)              : Buy or sell price to 8 decimal places precision.
        want_amount (int)        : Amount of tokens offered in the order.
        use_native_tokens (bool) : Whether to use SWTH as fees or not. Possible values are: true or false.
        order_type (str)         : Order type, possible values are: limit.
        contract_hash (str)      : Switcheo Exchange contract hash to execute the deposit on.

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object
        Check schemas.CREATE_ORDER_RESPONSE_SCHEMA
    """
    # The current timestamp to be used as a nonce as epoch milliseconds.
    timestamp = utils.get_current_epoch_milli()

    # TODO: (ansrivas) Check how to handle currencies which are not divisible, for eg. NEO ( until v3 is released)
    want_amount = utils.convert_to_neo_asset_amount(want_amount)
    price = Fixed8(price).value
    signable_params = {
        "blockchain": blockchain,
        "price": price,
        "side": side,
        "want_amount": want_amount,
        "use_native_tokens": use_native_tokens,
        "timestamp": timestamp,
        "order_type": order_type,
        "contract_hash": contract_hash,
        "pair": pair,
    }

    # The order creator's address. Do not include this in the parameters to be signed.
    # This needs to be the script hash of the public key
    address_script_hash = get_public_key_script_hash_from_wif(priv_key_wif)
    pk = get_private_key_from_wif(priv_key_wif)

    signable_params_json_str = utils.jsonify(signable_params)
    encoded_msg = encode_msg(signable_params_json_str)
    signature = sign_msg(encoded_msg, pk)

    params = {**signable_params, "signature": signature, "address": address_script_hash}

    logger.debug("Params being sent to create orders: {0}".format(params))
    url = utils.format_urls(base_url, orders.CREATE_ORDER)
    resp = requests.post(url, json=params)
    return utils.response_else_exception(resp)


def _execute_order(base_url, order, priv_key_wif):
    """This is the second endpoint required to execute an order.

    After using the Create Order endpoint, you will receive a response which needs to be signed.
    Every txn of the fills and makes in the Create Order response should be signed.

    Args:
        order (dict) : The response object returned after creating an order
    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

    """
    id = order["id"]
    fills, makes = order["fills"], order["makes"]
    logger.debug("Fills are {}".format(fills))
    logger.debug("makes are {}".format(makes))

    priv_key = get_private_key_from_wif(priv_key_wif)
    signatures = {
        "fills": sign_array(fills, priv_key),
        "makes": sign_array(makes, priv_key),
    }
    params = {"signatures": signatures}

    logger.debug("Params being sent to create deposit: {0}".format(params))
    url = utils.format_urls(base_url, orders.EXECUTE_ORDER.format(id=id))

    resp = requests.post(url, json=params)
    return utils.response_else_exception(resp)


def _create_cancellation(base_url, order_id, priv_key_wif):
    """This is the first API call required to cancel an order.

    Only orders with makes and with an available_amount of more than 0 can be cancelled.

    Args:
        order_id (str) : The order id which needs to be cancelled.
    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

    """
    signable_params = {
        "order_id": order_id,
        "timestamp": utils.get_current_epoch_milli(),
    }

    priv_key = get_private_key_from_wif(priv_key_wif)

    signable_params_json_str = utils.jsonify(signable_params)
    encoded_msg = encode_msg(signable_params_json_str)
    signature = sign_msg(encoded_msg, priv_key)

    address_script_hash = get_public_key_script_hash_from_wif(priv_key_wif)
    params = {**signable_params, "signature": signature, "address": address_script_hash}

    logger.debug("Params being sent to create deposit: {0}".format(params))
    url = utils.format_urls(base_url, orders.CREATE_CANCELLATION)
    resp = requests.post(url, json=params)
    return utils.response_else_exception(resp)


def _execute_cancellation(base_url, cancellation, priv_key_wif):
    """This is the second endpoint that must be called to cancel an order.

    After calling the Create Cancellation endpoint, you will receive a transaction in the resp which must be signed.

    Args:
        cancellation (dict) : The cancellation object which is received from create cancellation end point.
    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

    """
    logger.debug("cancellation transaction is {0}".format(utils.jsonify(cancellation["transaction"])))

    pk = get_private_key_from_wif(priv_key_wif)
    signature = sign_transaction(cancellation["transaction"], pk)

    url = utils.format_urls(base_url, orders.EXECUTE_CANCELLATION.format(id=cancellation["id"]))
    resp = requests.post(url, json={"signature": signature})
    return utils.response_else_exception(resp)
