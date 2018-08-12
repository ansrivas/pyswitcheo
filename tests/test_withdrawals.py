# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to withdrawal end points"""

from http import HTTPStatus
from jsonschema import validate
from pyswitcheo.utils import response_to_json
from pyswitcheo.internal.api import withdrawals
from pyswitcheo.schemas import CREATE_WITHDRAWAL_SCHEMA


# def test_create_withdrawal(url):
#     """Get last price for the resources."""
#
#     contract_hash = "a195c1549e7da61b8da315765a790ac7e7633b82"
#     # encrypted_key = b"6PYKozqwKwRYi77GN3AwTwXEssJZWbfneYKEYbiSeuNtVTGPFT2Q7EJpjY"
#
#     priv_key_wif = "L4FSnRosoUv22cCu5z7VEEGd2uQWTK7Me83vZxgQQEsJZ2MReHbu"
#     # address = "AG9YqjpmoQC5Ufxo2JUr8zCSrXba9krc7g"
#
#     withdrawals_response = withdrawals._create_withdrawal(base_url=url.testnet, asset_id="SWTH",
#                                                           contract_hash=contract_hash, amount=10,
#                                                           priv_key_wif=priv_key_wif, blockchain="neo")
#     json_response = response_to_json(withdrawals_response)
#     assert validate(json_response, CREATE_WITHDRAWAL_SCHEMA) is None, "Failed to validate response from withdrawals"
#     assert withdrawals_response.status_code == HTTPStatus.OK


def test_create_and_execute_withdrawal(url):
    """Create an execute followed by withdrawal transaction."""
    contract_hash = "a195c1549e7da61b8da315765a790ac7e7633b82"
    # encrypted_key = b"6PYKozqwKwRYi77GN3AwTwXEssJZWbfneYKEYbiSeuNtVTGPFT2Q7EJpjY"

    priv_key_wif = "L4FSnRosoUv22cCu5z7VEEGd2uQWTK7Me83vZxgQQEsJZ2MReHbu"
    # address = "AG9YqjpmoQC5Ufxo2JUr8zCSrXba9krc7g"

    withdrawals_response = withdrawals._create_withdrawal(base_url=url.testnet, asset_id="SWTH",
                                                          contract_hash=contract_hash, amount=10,
                                                          priv_key_wif=priv_key_wif, blockchain="neo")
    withdrawals_response_json_obj = response_to_json(withdrawals_response)
    assert validate(withdrawals_response_json_obj, CREATE_WITHDRAWAL_SCHEMA) is None, ("Failed to validate "
                                                                                       " response from withdrawals")
    assert withdrawals_response.status_code == HTTPStatus.OK

    # Now lets execute withdrawal
    exec_withdrawal_resp = withdrawals._execute_withdrawal(base_url=url.testnet,
                                                           withdrawal=withdrawals_response_json_obj,
                                                           priv_key_wif=priv_key_wif)
    assert exec_withdrawal_resp.status_code == HTTPStatus.OK
