======================
More Examples
======================


1.  Check balances
^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

    import json
    from http import HTTPStatus
    from pyswitcheo.api import SwitcheoApi

    if __name__ == '__main__':
        client = SwitcheoApi(base_url="https://test-api.switcheo.network")

        pubkey = "ANVLCD3xqGXKhDnrivpVFvDLcvkpgPbbMt"
        contract_hash = ["a195c1549e7da61b8da315765a790ac7e7633b82"]

        resp = client.list_balances(addresses=pubkey, contract_hashes=contract_hash)
        if resp.status_code == HTTPStatus.OK:
            print(json.loads(resp.text.encode("UTF-8")))

2.  List available contracts on switcheo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

    import json
    from http import HTTPStatus
    from pyswitcheo.api import SwitcheoApi

    if __name__ == '__main__':
        client = SwitcheoApi(base_url="https://test-api.switcheo.network")

        resp = client.list_contracts()
        if resp.status_code == HTTPStatus.OK:
            print(json.loads(resp.text.encode("UTF-8")))

3. Create deposit to Switcheo smart contract for trading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

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


4. Interacting with orders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python


    from pyswitcheo.api import SwitcheoApi
    from pyswitcheo.utils import response_to_json


    def list_order(client, address, contract_hash):
        """List order example."""

        response = client.list_orders(address=address, contract_hash=contract_hash, pair="SWTH_NEO")
        orders = response_to_json(response)

        # for eg. print only orders which were of type sell
        # Here lots of operations can be applied
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
        create_order_resp = client.create_order(priv_key_wif=priv_key_wif, pair="SWTH_NEO", asset_id="SWTH",
                                                blockchain="neo", side="sell", price=0.01, want_amount=0.05,
                                                use_native_tokens=True, order_type="limit", contract_hash=contract_hash)

        order_object = response_to_json(create_order_resp)

        # This order object then can be used to cancel orders
        # client.create_cancellation(order_id=order_object["id"], priv_key_wif=priv_key_wif)




4. Get tickers information, like candlesticks, etc.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

    import json
    from http import HTTPStatus
    from pyswitcheo.api import SwitcheoApi

    if __name__ == '__main__':
        client = SwitcheoApi(base_url="https://test-api.switcheo.network")
        resp = client.get_candle_sticks(pair="SWTH_NEO", start_time=1433736037,
                                        end_time=1533736037,
                                        interval=1440)
        if resp.status_code == HTTPStatus.OK:
            print(json.loads(resp.text.encode("UTF-8")))



5. Withdraw from switcheo smart-contract to your wallet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. code-block:: python

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
