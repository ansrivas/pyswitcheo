# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deposits allows movement of funds from your wallet into the Switcheo smart contract.
This movement of funds is free of charge. Trading on Switcheo Exchange can only be done
using funds that have been successfully deposited into the smart contract.
Deposits are not instantaneous. Once a deposit has been executed, funds in your wallet
balance would be deducted by the amount of tokens you chose to deposit. Funds deducted
from your wallet balance will be added to your contract balance but put on hold until
Switcheo has determined that it has been successfully broadcasted to the blockchain.
"""
import logging
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls import deposits
from pyswitcheo.serialization import sign_msg, serialize_transaction
from pyswitcheo.crypto_utils import (
    encode_msg,
    get_private_key_from_wif,
    get_public_key_script_hash_from_wif,
)

logger = logging.getLogger(__name__)

# TODO: (ansrivas) Give an option to load from wallet, pass wif and pass private key


def _create_deposit(base_url, priv_key_wif, asset_id, amount, contract_hash, blockchain="NEO"):
    """This endpoint creates a deposit which can be executed through Execute Deposit.

    To be able to make a deposit, sufficient funds are required in the depositing wallet.
    NOTE: After calling this endpoint, the Execute Deposit endpoint has to be called for the deposit to be executed.

    Args:
        base_url (str)      : This paramter governs whether to connect to test or mainnet..
        priv_key_wif (str)  : The private key wif of the user.
        asset_id (str)      : The asset symbol or ID to deposit. for eg. SWTH
        amount (int)        : Amount of tokens to deposit.
        contract_hash (str) : Switcheo Exchange contract hash to execute the deposit on.
        blockchain (str)    : Blockchain that the token to deposit is on. Possible values are: neo.

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object
        Check schemas.CREATE_DEPOSIT_SCHEMA
    """

    signable_params = {
        "blockchain": blockchain,
        "asset_id": asset_id,
        "amount": utils.convert_to_neo_asset_amount(amount),
        "timestamp": utils.get_current_epoch_milli(),
        "contract_hash": contract_hash,
    }
    signable_params_json_str = utils.jsonify(signable_params)

    # The depositer's address. Do not include this in the parameters to be signed.
    # This needs to be the script hash of the public key
    address_script_hash = get_public_key_script_hash_from_wif(priv_key_wif)

    pk = get_private_key_from_wif(priv_key_wif)
    encoded_msg = encode_msg(signable_params_json_str)
    signature = sign_msg(encoded_msg, pk)

    params = {**signable_params, "signature": signature, "address": address_script_hash}

    logger.debug("Params being sent to create deposit: {0}".format(params))
    url = utils.format_urls(base_url, deposits.CREATE_DEPOSIT)
    resp = requests.post(url, json=params)
    return utils.response_else_exception(resp)


def _execute_deposit(base_url, deposit, priv_key_wif):
    """This is the second endpoint required to execute a deposit. After using the Create Deposit endpoint,
    you will receive a response which requires additional signing.
    The signature should then be attached as the signature parameter in the request payload.

    Note that a sha256 parameter is provided for convenience to be used directly as part of the ECDSA signature
    process. In production mode, this should be recalculated for additional security.

    Args:
        base_url (str)     : This paramter governs whether to connect to test or mainnet..
        deposit (json)     : The correct json response returned from create_deposit function (json.loads)
        priv_key_wif (str) : The private key WIF of the user.

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

    """
    logger.debug("Deposit transaction is {0}".format(utils.jsonify(deposit["transaction"])))

    pk = get_private_key_from_wif(priv_key_wif)
    # signature is Signed response from create deposit endpoint.
    # signable_params_json_str = utils.jsonify(deposit["transaction"])

    signature = sign_msg(serialize_transaction(deposit["transaction"], False), pk)

    url = utils.format_urls(base_url, deposits.EXECUTE_DEPOSIT.format(id=deposit["id"]))
    resp = requests.post(url, json={"signature": signature})
    return utils.response_else_exception(resp)
