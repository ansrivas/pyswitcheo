# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to crypto.py file."""


from pyswitcheo.serialization import serialize_transaction  # , sign_msg
# from pyswitcheo.crypto_utils import get_private_key_from_wif, encode_msg


expected_serialized = ("d101520800ca9a3b000000001432e125258b7db0a0dffde5bd03"
                       "b2b859253538ab1449a7f81f67944e02c9d7da02b14dc87d20ae44d153c1076"
                       "465706f73697467823b63e7c70a795a7615a38d1ba67d9e54c195a100000000"
                       "00000000012049a7f81f67944e02c9d7da02b14dc87d20ae44d102d0845fec2d"
                       "3221cec384f50849b0944903d131bbc0eb10a144b2b05557e16f470000e92f29"
                       "f3470efaf252a4b22aa0fe359740fc06b6aac305bf4c593e5ab012e4042f0001e"
                       "72d286979ee6cb1b7e65dfddfb2e384100b8d148e7758de42e4168b71792c6001"
                       "000000000000007335f929546270b8f811a0f9427b5712457107e7")
input_json_response = {
    "id": "d85f76d2-1c13-432d-a17f-a54009734f59",
    "transaction": {
        "hash": "71d280abc0a6d6063573faf7c0c3d5ecc3fb8e9f505728ec4f5a3f04f0daef23",
        "sha256": "e2c7cfa234ffe2bc00441580b3ad0b8bbd436a5d4ff1933ef92219349e9d3fd3",
        "type": 209,
        "version": 1,
        "attributes": [{
            "usage": 32,
            "data": "49a7f81f67944e02c9d7da02b14dc87d20ae44d1"
        }],
        "inputs": [{
            "prevHash": "476fe15755b0b244a110ebc0bb31d1034994b04908f584c3ce21322dec5f84d0",
            "prevIndex": 0
        },
            {
            "prevHash": "04e412b05a3e594cbf05c3aab606fc409735fea02ab2a452f2fa0e47f3292fe9",
            "prevIndex": 47
        }
        ],
        "outputs": [{
            "assetId": "602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7",
            "scriptHash": "e707714512577b42f9a011f8b870625429f93573",
            "value": 1e-08
        }],
        "scripts": [],
        "script": ("0800ca9a3b000000001432e125258b7db0a0dffde5bd03b2b859253538ab1449a7f81f67944e02c9d7da02b14"
                   "dc87d20ae44d153c1076465706f73697467823b63e7c70a795a7615a38d1ba67d9e54c195a1"),
        "gas": 0
    },
    "script_params": {
        "scriptHash": "a195c1549e7da61b8da315765a790ac7e7633b82",
        "operation": "deposit",
        "args": ["49a7f81f67944e02c9d7da02b14dc87d20ae44d1", "32e125258b7db0a0dffde5bd03b2b859253538ab", 1000000000]
    }
}


def test_serialize_transaction():
    """Test transaction serialization."""
    got = serialize_transaction(input_json_response["transaction"], signed=False)
    assert expected_serialized == got, "Expected {0} but received {1} for input {2}".format(expected_serialized, got)


# FIXME: (ansrivas)
# def test_sign_message():
#     """Test message signing."""
#     wif = "L2vHHz8L4rtkUkFaxzQoPro33bo7McYMRoUU69DjE334a8NT8zc9"
#
#     # msg_to_sign = "Sample message to sign"
#     msg_to_sign = expected_serialized
#     encoded_msg = msg_to_sign
#     encoded_msg = encode_msg(msg_to_sign)
#
#     expected_signature = ('b4a6c57b0262890a2237e9d8eb9c8c82b0f0846ac83ba177b95789d9a9dae5583aa'
#                           'e65a91d4cffb861df64d02165b84f579da3047fe8cbb2bbf4b53e1ae0a9a8')
#
#     pk = get_private_key_from_wif(wif)
#
#     got = sign_msg(msg=encoded_msg, priv_key=pk)
#     assert expected_signature == got, "Expected {0} but received {1} for input {2}".format(expected_signature, got,
    # msg_to_sign)
