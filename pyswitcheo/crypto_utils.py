# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Crypto related wrapper functions."""

import re
import string
import logging
import base58
import hashlib
import binascii
from neocore.KeyPair import KeyPair

logger = logging.getLogger(__name__)

__HEX_STRING_REGEX_OBJ = re.compile(r"^([0-9A-Fa-f]{2})*$/")
MAX_TRANSACTION_ATTRIBUTE_SIZE = 65535


def is_hex(input_hex):
    """Check if the passed string is a hex string.

    Empty string is always treated as hex.
    """
    if input_hex == "":
        return True

    return all(c in set(string.hexdigits) for c in input_hex)


def ensure_hex(input_hex):
    """Check if the passed string is a hex string else raise exception.

    Empty string is always treated as hex.
    """

    if not is_hex(input_hex):
        raise Exception(
            "Expected a hexstring but got {input_hex}.".format(input_hex=input_hex)
        )


def reverse_hex(input_hex):
    """Reverse a HEX string, treating 2 chars as a byte.

    Expected results look like this:
    reverse_hex('abcdef') = 'efcdab'

    Args:
        input_hex (str): Input string in hex which needs to be converted.

    Returns:
        Hex string reversed.
    """
    return "".join([input_hex[x: x + 2] for x in range(0, len(input_hex), 2)][::-1])


def num_to_hex_string(num, size=1, little_endian=False):
    """Convert a given number to hex string.

    Converts a number to a big endian hexstring of a suitable size, optionally little endian

    Args:
        num (int)   : Input int for which we need to get the hex string
        size  (int) : The required size in bytes, eg 1 for Uint8, 2 for Uint16. Defaults to 1.
    Returns:
        (str)

    """
    if num < 0:
        raise Exception("num should be unsigned (>= 0)")

    if size % 1 != 0:
        raise TypeError("size must be a whole integer")

    size = size * 2
    hexstring = hex(num)[2:]
    hexstr_len = len(hexstring)

    output = (
        hexstring if hexstr_len % size == 0 else ("0" * (size) + hexstring)[hexstr_len:]
    )
    if little_endian:
        return reverse_hex(output)
    return output


def num_to_var_int(num):
    """Convert a number to a variable length Int. Used for array length header.

    Detailed explanation

    Args:
        num (int) : A number
    Returns:
        (str) hexstring of the variable Int
    """
    if num < 0xfd:
        return num_to_hex_string(num)
    elif num <= 0xffff:
        # uint16
        return "fd" + num_to_hex_string(num, 2, True)
    elif num <= 0xffffffff:
        # uint32
        return "fe" + num_to_hex_string(num, 3, True)
    else:
        # uint64
        return "ff" + num_to_hex_string(num, 8, True)


def encode_msg(msg):
    """Convert a given msg to its hex representation.

    This is generally used when we send signed payload to the Switcheo api.

    Args:
        msg (str) : Input message which needs to be encoded.
    Returns:
        encoded message (str)
    """
    if isinstance(msg, str):
        msg = msg.encode("UTF-8")

    encoded_msg = binascii.hexlify(msg)
    length_hex = hex(int(len(encoded_msg) / 2))[2:]
    logger.debug("Length of hex message {0}".format(length_hex))

    encoded_msg = "010001f0{hex_len}{enc_msg}0000".format(
        hex_len=length_hex, enc_msg=encoded_msg.decode()
    )
    logger.debug("Final message to sign : {0}".format(encoded_msg))
    return encoded_msg


def get_private_key_from_wif(wif):
    """Fetch the private key from a wif represented in string format.

    Args:
        wif (str) : wif from which we need to extract the private key

    Returns:
        private key in bytearray format
    """
    pk = KeyPair.PrivateKeyFromWIF(wif)
    return KeyPair(pk).PrivateKey


def get_wif_from_private_key(priv_key):
    """Convert the given privatekey to a wif format.

    Args:
        priv_key (str) : private key in its hex string format.
    Returns:
        WIF format
    """

    # Step 1: let's add 80 in front of it and 01 in the end
    extended_key = "80" + priv_key + "01"
    # Step 2: first SHA-256
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    # Step 3: second SHA-256
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # Step 4-5: add checksum to end of extended key
    final_key = extended_key + second_sha256[:8]
    # Step 6: finally the Wallet Import Format is the base 58 encode of final_key
    return base58.b58encode(binascii.unhexlify(final_key))


def get_public_key_script_hash_from_wif(wif):
    """Fetch the script hash of the public key from a wif represented in string format.

    Args:
        wif (str) : wif from which we need to extract the public key script hash

    Returns:
        public key script hash in string format
    """
    pk = KeyPair.PrivateKeyFromWIF(wif)
    keypair = KeyPair(pk)
    logger.debug("Public Address is {}".format(keypair.GetAddress()))
    return get_script_hash_from_address(keypair.GetAddress())


def get_script_hash_from_address(address):
    """Convert a given address to script hash.
    This code has been taken from:
    https://github.com/CityOfZion/neo-python-core/blob/fcb0837e8f69e6f4dc01f2861b856affd2213446/neocore/bin/cli.py#L23
    """
    data = bytes(base58.b58decode(address))

    # Make sure signature byte is correct. In python 3, data[0] is bytes, and in 2 it's str.
    # We use this isinstance checke to make it work with both Python 2 and 3.
    is_correct_signature = data[0] != 0x17 if isinstance(data[0], bytes) else b"\x17"
    if not is_correct_signature:
        raise Exception("Invalid address: wrong signature byte")

    # Make sure the checksum is correct
    if data[-4:] != hashlib.sha256(hashlib.sha256(data[:-4]).digest()).digest()[:4]:
        raise Exception("Invalid address: invalid checksum")

    # Return only the scripthash bytes, reverse it and return hex of it.
    return data[1:-4][::-1].hex()
