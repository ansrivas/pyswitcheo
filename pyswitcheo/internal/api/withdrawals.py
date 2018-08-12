# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Withdrawals allow free movement of tokens from the Switcheo smart contract into your wallet.
This movement of tokens is free of charge.
Once a withdrawal has been executed, tokens in your contract balance would be deducted.
Tokens that are put on hold by orders cannot be withdrawn.
Withdrawals are not instantaneous. Tokens deducted from your contract balance will be added to your wallet balance but
put on hold until the withdrawal has been fully executed.
"""

import logging
import requests
from pyswitcheo import utils
from pyswitcheo.serialization import sign_msg
from pyswitcheo.internal.urls import withdrawals
from pyswitcheo.crypto_utils import (
    encode_msg,
    get_private_key_from_wif,
    get_public_key_script_hash_from_wif,
)

logger = logging.getLogger(__name__)


def _create_withdrawal(base_url, priv_key_wif, asset_id, amount, contract_hash, blockchain="NEO"):
    """Creates a withdrawal which can be executed later through execute_withdrawal.

    To be able to make a withdrawal, sufficient funds are required in the contract balance.
    A signature of the request payload has to be provided for this API call.

    Args:
        base_url (str)      : This paramter governs whether to connect to test or mainnet..
        priv_key_wif (str)      : The private key wif of the user.
        asset_id (str)      : The asset symbol or ID to withdraw. for eg. SWTH
        amount (int)        : Amount of tokens to withdraw.
        contract_hash (str) : Switcheo Exchange contract hash to execute the withdraw on.
        blockchain (str)    : Blockchain that the token to withdraw is on. Possible values are: neo.

    Returns:
        An id representing this transaction
        Example response:
        {
          "id": "e0f56e23-2e11-4848-b749-a147c872cbe6"
        }

    """
    signable_params = {
        "blockchain": blockchain,
        "asset_id": asset_id,
        "amount": utils.convert_to_neo_asset_amount(amount),
        "timestamp": utils.get_current_epoch_milli(),
        "contract_hash": contract_hash,
    }
    signable_params_json_str = utils.jsonify(signable_params)

    # The withdrawer's address. Do not include this in the parameters to be signed.
    address_script_hash = get_public_key_script_hash_from_wif(priv_key_wif)

    pk = get_private_key_from_wif(priv_key_wif)
    encoded_msg = encode_msg(signable_params_json_str)
    signature = sign_msg(encoded_msg, pk)

    params = {**signable_params, "signature": signature, "address": address_script_hash}

    logger.debug("Params being sent to create withdrawal: {0}".format(params))
    url = utils.format_urls(base_url, withdrawals.CREATE_WITHDRAWAL)
    resp = requests.post(url, json=params)
    return utils.response_else_exception(resp)


def _execute_withdrawal(base_url, withdrawal, priv_key_wif):
    """This is the second endpoint required to execute a withdrawal.

    After using the Create Withdrawal endpoint, you will receive a response which requires additional signing.

    Note that a sha256 parameter is provided for convenience to be used directly as part of the ECDSA signature
    process. In production mode, this should be recalculated for additional security.

    Args:
        base_url (str)    : This paramter governs whether to connect to test or mainnet.
        withdrawal (dict) : Withdrawal is the json object returned after executing create_withdrawal end point.
        priv_key_wif (str)    : The private key of the user. (wif)

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

    """
    logger.debug("Withdrawal invoke transaction is {0}".format(utils.jsonify(withdrawal)))

    pk = get_private_key_from_wif(priv_key_wif)

    signable_params = {
        "id": withdrawal["id"],
        "timestamp": utils.get_current_epoch_milli()
    }
    signable_params_json_str = utils.jsonify(signable_params)
    encoded_signable_params = encode_msg(signable_params_json_str)
    signature = sign_msg(encoded_signable_params, pk)

    params = {"signature": signature, **signable_params}
    logger.debug("Final params being sent to execute withdrawal {0}".format(params))
    url = utils.format_urls(base_url, withdrawals.EXECUTE_WITHDRAWAL.format(id=withdrawal["id"]))
    resp = requests.post(url, json=params)
    return utils.response_else_exception(resp)
