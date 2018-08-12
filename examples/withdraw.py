# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example to interact with withdrawals."""

from pyswitcheo.api import SwitcheoApi


if __name__ == '__main__':
    client = SwitcheoApi(base_url="https://test-api.switcheo.network")

    # Use this example for listing orders

    contract_hash = 'a195c1549e7da61b8da315765a790ac7e7633b82'
    priv_key_wif = 'L4FSnRosoUv22cCu5z7VEEGd2uQWTK7Me83vZxgQQEsJZ2MReHbu'
    address = "AG9YqjpmoQC5Ufxo2JUr8zCSrXba9krc7g"

    # Make sure that you have something deposited in the contract before invoking this
    deposit_response = client.deposit(priv_key_wif=priv_key_wif, asset_id="SWTH", amount=10,
                                      contract_hash="a195c1549e7da61b8da315765a790ac7e7633b82",
                                      blockchain="neo")
    print("Response from deposit transaction {}".format(deposit_response.text))

    withdraw_response = client.withdraw(asset_id="SWTH",
                                        contract_hash=contract_hash, amount=10,
                                        priv_key_wif=priv_key_wif, blockchain="neo")

    print("Response from withdraw transaction {}".format(withdraw_response.text))
