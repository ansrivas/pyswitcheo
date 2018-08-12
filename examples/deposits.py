# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example to create deposits Switcheo Dex."""

from pyswitcheo.api import SwitcheoApi

if __name__ == '__main__':
    client = SwitcheoApi(base_url="https://test-api.switcheo.network")

    # encrypted_key = b"6PYKozqwKwRYi77GN3AwTwXEssJZWbfneYKEYbiSeuNtVTGPFT2Q7EJpjY"
    # pub_key = "ANVLCD3xqGXKhDnrivpVFvDLcvkpgPbbMt"
    # priv_key_wif = "L2vHHz8L4rtkUkFaxzQoPro33bo7McYMRoUU69DjE334a8NT8zc9"

    # priv_key_wif = get_wif_from_private_key("L4FSnRosoUv22cCu5z7VEEGd2uQWTK7Me83vZxgQQEsJZ2MReHbu")
    priv_key_wif = 'L4FSnRosoUv22cCu5z7VEEGd2uQWTK7Me83vZxgQQEsJZ2MReHbu'
    deposit_response = client.deposit(priv_key_wif=priv_key_wif, asset_id="SWTH", amount=10,
                                      contract_hash="a195c1549e7da61b8da315765a790ac7e7633b82",
                                      blockchain="neo")
    print(deposit_response.text)
