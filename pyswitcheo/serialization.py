# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Crypto related wrapper functions."""

import logging
import pyswitcheo.crypto_utils as cutils
from neocore.Cryptography.Crypto import Crypto
from pyswitcheo.datatypes.fixed8 import Fixed8
from pyswitcheo.datatypes.transaction_types import (
    TransactionInput,
    TransactionOutput,
    TransactionAttribute,
    Witness,
)

logger = logging.getLogger(__name__)

MAX_TRANSACTION_ATTRIBUTE_SIZE = 65535


def serialize_transaction_output(output):
    """Serialize an object of type TransactionOutput

    TransactionOutput has three params
    1. assetId: assetId, Uint256
    2. value: value of output, Fixed8
    3. scriptHash of type Uint160

    Args:
        input (TransactionOutput) : TransactionOutput which needs to be serialized.
    Returns:
        (str) serialized version of TransactionOutput
    """
    value = Fixed8(output.value).to_reverse_hex()
    return "".join(
        [
            cutils.reverse_hex(output.assetId),
            value,
            cutils.reverse_hex(output.scriptHash),
        ]
    )


def serialize_transaction_input(input):
    """Serialize an object of type TransactionInput

    TransactionInput has two params
    1. prevHash: Transaction hash (Uint256)
    2. prevIndex:  Index of the coin in the previous transaction (Uint16)

    Args:
        input (TransactionInput) : TransactionInput which needs to be serialized.
    Returns:
        (str) serialized version of TransactionInput
    """
    logger.debug("serialize_transaction_input")
    logger.debug(cutils.reverse_hex(input.prevHash))
    logger.debug(cutils.reverse_hex(cutils.num_to_hex_string(input.prevIndex, 2)))
    return cutils.reverse_hex(input.prevHash) + cutils.reverse_hex(
        cutils.num_to_hex_string(input.prevIndex, 2)
    )


def serialize_claim_exclusive():
    """."""
    pass


def serialize_contract_exclusive():
    """."""
    pass


def serialize_invocation_exclusive(transaction):
    """Short explanation.

    Detailed explanation

    Args:

    Returns:

    """
    if transaction["type"] != 0xd1:
        raise TypeError("TransactionInvocation type should be 0xd1.")
    out = cutils.num_to_var_int(int(len(transaction["script"]) / 2))
    out += transaction["script"]
    if transaction["version"] >= 1:
        out += str(Fixed8.num_to_fixed_8(transaction["gas"]))
    return out


def serialize_exclusive(transaction_type):
    """."""
    op_type = {
        2: serialize_claim_exclusive,
        128: serialize_contract_exclusive,
        209: serialize_invocation_exclusive,
    }
    return op_type[transaction_type]


def serialize_witness(witness):
    """Serialize an object of type Witness

    Witness object has two params
    1. invocationScript:  This data is stored as is (Little Endian)
    2. verificationScript: This data is stored as is (Little Endian)

    Args:
        input (witness) : witness which needs to be serialized.
    Returns:
        (str) serialized version of witness
    """
    invo_len = cutils.num_to_var_int(len(witness.invocationScript) / 2)
    veri_len = cutils.num_to_var_int(len(witness.verificationScript) / 2)
    return invo_len + witness.invocationScript + veri_len + witness.verificationScript


def sign_transaction(transaction, priv_key):
    """Sign a transaction object returned as a part of any transaction creation using user's private key.

    Args:
        transaction (json) : Transaction is dictionary object which is returned after creating a transaction.
        priv_key (bytes)  : Private key to be used to sign this.
    Returns:
        A signed transaction string
    """
    serialized_tx_msg = serialize_transaction(tx=transaction, signed=False)
    return sign_msg(serialized_tx_msg, priv_key)


def sign_msg(msg, priv_key):
    """Sign a given message using a private key.

    Args:
        msg (str)         : Message which needs to be signed.
        priv_key (bytes)  : Private key to be used to sign this.

    Returns:
        Signed message as a byte array.
    """
    return Crypto.Sign(msg, priv_key).hex()


def serialize_transaction_attribute(attr):
    """Serialize a TransactionAttribute

    Detailed explanation

    Args:

    Returns:
        str
    """
    attr_len = len(attr.data)
    if attr_len > MAX_TRANSACTION_ATTRIBUTE_SIZE:
        raise Exception(
            "Attribute data size is beyond max attribute size {0}".format(
                MAX_TRANSACTION_ATTRIBUTE_SIZE
            )
        )

    out = cutils.num_to_hex_string(attr.usage)
    if attr.usage == 0x81:
        out += cutils.num_to_hex_string(attr_len / 2)
    elif attr.usage == 0x90 or attr.usage >= 0xf0:
        out += cutils.num_to_var_int(attr_len / 2)

    if (attr.usage == 0x02) or (attr.usage == 0x03):
        out += attr.data[2:64]
    else:
        out += attr.data

    return out


def serialize_transaction(tx, signed=True):
    """Serialize a transaction object

    Whenever an operation is invoked on the blockchain, we get a transaction object.
    As a rest response we can pass this here to sign it.

    Args:

    Returns:

    """
    tx_out = tx["outputs"]
    tx_ins = tx["inputs"]
    tx_scripts = tx["scripts"]

    out = ""
    out += cutils.num_to_hex_string(tx["type"])

    out += cutils.num_to_hex_string(tx["version"])

    out += (serialize_exclusive(tx["type"]))(tx)

    out += cutils.num_to_var_int(len(tx["attributes"]))

    for attribute in tx["attributes"]:
        attr = TransactionAttribute(**attribute)
        out += serialize_transaction_attribute(attr)

    out += cutils.num_to_var_int(len(tx_ins))

    for tx_in in tx_ins:
        inp = TransactionInput(**tx_in)
        out += serialize_transaction_input(inp)

    out += cutils.num_to_var_int(len(tx_out))

    for output in tx_out:
        outp = TransactionOutput(**output)
        out += serialize_transaction_output(outp)

    if signed and tx_scripts and (len(tx_scripts) > 0):
        out += cutils.num_to_var_int(len(tx_scripts))
        for script in tx_scripts:
            witness = Witness(**script)
            out += serialize_witness(witness)

    logger.debug("Final serialized transaction message to sign {0}".format(out))
    return out.strip()


def sign_array(input_arr, priv_key):
    """Sign each item in an input array.

    Args:
        input_arr (dict) : An input array with transaction objects. This is a dictionary with "txn" key in it.
    Returns:
        A dictionary of signed objects, where key is the id of each element in the input_arr.
    """
    signed_map = {}
    for item in input_arr:
        signed_map[item["id"]] = sign_transaction(item["txn"], priv_key)
    return signed_map
