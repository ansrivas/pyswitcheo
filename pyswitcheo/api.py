# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base API implementation for pyswitcheo."""

from pyswitcheo.internal.api import balances
from pyswitcheo.internal.api import contracts
from pyswitcheo.internal.api import deposits
from pyswitcheo.internal.api import offers
from pyswitcheo.internal.api import pairs
from pyswitcheo.internal.api import tickers
from pyswitcheo.internal.api import trades
from pyswitcheo.internal.api import orders
from pyswitcheo.internal.api import withdrawals
from pyswitcheo.utils import response_to_json


class SwitcheoApi(object):
    """Base implementation for interacting with pyswitcheo APIs."""

    def __init__(self, base_url, api_version="v2"):
        """Initialize Api class instances.
        Args:
            base_url(str)    : Base url represents the endpoint to query the Switcheo API server.
            api_version(str) : An optional api version which could change in future
        """
        self.base_url = str(base_url).strip("/") + '/' + api_version.strip("/")

    def get_candle_sticks(self, pair, start_time, end_time, interval):
        """Get candlestick chart data filtered by url parameters.

        Args:
            pair (str)	       : Show chart data of this trading pair
            start_time (int)   : Start of time range for data in epoch seconds
            end_time (int)	   : End of time range for data in epoch seconds
            interval (int)	   : Candlestick period in minutes Possible values are: 1, 5, 30, 60, 360, 1440

        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object

            Example response:
            [
              {
                "time": "1531215240",
                "open": "0.00049408",
                "close": "0.00049238",
                "high": "0.000497",
                "low": "0.00048919",
                "volume": "110169445.0",
                "quote_volume": "222900002152.0"
              },
              {
                "time": "1531219800",
                "open": "0.00050366",
                "close": "0.00049408",
                "high": "0.00050366",
                "low": "0.00049408",
                "volume": "102398958.0",
                "quote_volume": "205800003323.0"
              },
              ...
            ]
        """
        return tickers._get_candle_sticks(
            base_url=self.base_url,
            pair=pair,
            start_time=start_time,
            end_time=end_time,
            interval=interval
        )

    def list_contracts(self):
        """Fetch updated hashes of contracts deployed by Switcheo.

        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object

            Example response
            {
              "NEO":
              {
                "V1": "0ec5712e0f7c63e4b0fea31029a28cea5e9d551f",
                "V1_5": "c41d8b0c30252ce7e8b6d95e9ce13fdd68d2a5a8",
                "V2": "48756743d524af03aa75729e911651ffd3cbe7d8"
              }
            }
        """
        return contracts._list_contracts(self.base_url)

    def list_pairs(self, bases):
        """Fetch available currency pairs on Switcheo Exchange filtered by the base parameter. Defaults to all pairs.

        Args:
            base_url (str)    : This paramter governs whether to connect to test or mainnet..
            bases (list[str]) : Provides pairs for these base symbols. Possible values are NEO, GAS, SWTH, USD.

        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object

            Example response
            [
              "GAS_NEO",
              "SWTH_NEO"
            ]
        """
        pairs._list_currency_pairs(self.base_url, bases)

    def list_balances(self, addresses, contract_hashes):
        """List contract balances of the given address and contract hashes.

        Args:
            base_url (str)               : This paramter governs whether to connect to test or mainnet..
            addresses (list[str])        : Only return balances for these addresses.
            contract_hashes (list[str])  : Only return balances from these contract hashes.

        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object

            Example response:
            {
              "confirming": {
                "GAS": [
                  {
                    "event_type": "withdrawal",
                    "asset_id": "602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7",
                    "amount": -100000000,
                    "transaction_hash": null,
                    "created_at": "2018-07-12T10:48:48.866Z"
                  }
                ]
              },
              "confirmed": {
                "GAS": "47320000000.0",
                "SWTH": "421549852102.0",
                "NEO": "50269113921.0"
              },
              "locked": {
                "GAS": "500000000.0",
                "NEO": "1564605000.0"
              }
            }
        """
        assert isinstance(addresses, list), "addresses should be a list object for eg. {}".format([addresses])
        assert isinstance(contract_hashes, list), "contract_hashes should be a list object for eg. [contract_hashes]"
        return balances._list_balances(self.base_url, addresses, contract_hashes)

    def list_trades(self, contract_hash, pair, from_time=None, to_time=None, limit=None):
        """Retrieve trades that have already occurred on Switcheo Exchange filtered by the request parameters.

        Args:
            contract_hash (str) : Only return trades for this contract hash.
            pair (str)          : Only return trades for this pair.
            from_time (int)     : Only return trades after this time in epoch seconds.
            to_time (int)       : Only return trades before this time in epoch seconds.
            limit (int)         : Only return this number of trades (min: 1, max: 10000, default: 5000).

        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object

            Example response:
            [
              {
                "id": "712a5019-3a23-463e-b0e1-80e9f0ad4f91",
                "fill_amount": 9122032316,
                "take_amount": 20921746,
                "event_time": "2018-06-08T11:32:03.219Z",
                "is_buy": false
              },
              {
                "id": "5d7e42a2-a8f3-40a9-bce5-7304921ff691",
                "fill_amount": 280477933,
                "take_amount": 4207169,
                "event_time": "2018-06-08T11:31:42.200Z",
                "is_buy": false
              },
              ...
            ]
        """
        return trades._list_trades(base_url=self.base_url, contract_hash=contract_hash, pair=pair,
                                   from_time=from_time, to_time=to_time, limit=limit)

    def deposit(self, priv_key_wif, asset_id, amount, contract_hash, blockchain="NEO"):
        """This api creates a deposit of provided asset on smart-contract.

        To be able to make a deposit, sufficient funds are required in the depositing wallet.
        This method performs two tasks 1. Creates a deposit on smart-contract 2. Executes it.

        Args:
            priv_key_wif (str)  : The private key wif of the user.
            asset_id (str)      : The asset symbol or ID to deposit. for eg. SWTH
            amount (int)        : Amount of tokens to deposit.
            contract_hash (str) : Switcheo Exchange contract hash to execute the deposit on.
            blockchain (str)    : Blockchain that the token to deposit is on. Possible values are: neo.

        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object
        """
        deposits_resp = deposits._create_deposit(base_url=self.base_url, priv_key_wif=priv_key_wif,
                                                 asset_id=asset_id, amount=amount, contract_hash=contract_hash,
                                                 blockchain=blockchain)
        return deposits._execute_deposit(base_url=self.base_url,
                                         deposit=response_to_json(deposits_resp), priv_key_wif=priv_key_wif,)

    def list_offers(self, blockchain, pair, contract_hash):
        """Retrieves the best 70 offers (per side) on the offer book.

        Args:
            blockchain (str)   : Only return offers from this blockchain. Possible values are neo.
            pair (str)         : Only return offers from this pair, for eg. SWTH_NEO
            contract_hash (str): Only return offers for contract hash. e.g. eed0d2e14b0027f5f30ade45f2b23dc57dd54ad2

        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object

            Example response:
            [
                {
                 "id": "b3a91e19-3726-4d09-8488-7c22eca76fc0",
                 "offer_asset": "SWTH",
                 "want_asset": "NEO",
                 "available_amount": 2550000013,
                 "offer_amount": 4000000000,
                 "want_amount": 320000000
                }
            ]
        """
        return offers._list_offers(self.base_url, blockchain, pair, contract_hash)

    def list_orders(self, address, contract_hash, pair=None):
        """Retrieves the best 70 offers (per side) on the offer book.

        Args:
            address (str)      : Only returns orders made by this address.
            contract_hash (str): Only return offers for the contract hash. e.g. eed0d2e14b0027f5f30ad2b23dc57dd54ad2
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
                "offer_asset_id": "c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b",
                "want_asset_id": "602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7",
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
        return orders._list_orders(self.base_url, address, contract_hash, pair=None)

    def create_order(self, priv_key_wif, pair, side, price, want_amount,
                     use_native_tokens, contract_hash, blockchain="neo", order_type='limit'):
        """Create an order on SWTH DEX.

        Orders can only be created after sufficient funds have been deposited into the user's contract
        balance. A successful order will have zero or one make and/or zero or more fills.

        NOTE: Based on the params you are using, let's say you are trying to sell SWTH for NEO at the price of 0.01
        exchange rate. The `want_amount` for a sell would be the amount of NEO you want. For eg
        we want_amount of neo = 0.1 and we want to sell 1 SWTH for 0.0005 NEOs. In this case the sell order would
        become at 0.0005 exchange rate for 0.1 NEO and 200 SWTH ( so you need to have 200 SWTH in your smart-contract)

        Args:
            base_url (str)           : This paramter governs whether to connect to test or mainnet.
            priv_key_wif (str)       : The private key wif of the user.
            pair (str)               : The pair to buy or sell on.
            blockchain (str)         : Blockchain that the pair is on. Possible values are: neo.
            side (str)               : Whether to buy or sell on this pair. Possible values are: buy, sell.
            price (str)              : Buy or sell price to 8 decimal places precision.
            want_amount (int)        : Amount of tokens offered in the order.
            use_native_tokens (bool) : Whether to use SWTH as fees or not. Possible values are: true or false.
            order_type (str)         : Order type, possible values are: limit.
            contract_hash (str)      : Switcheo Exchange contract hash to execute the deposit on.

        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object
        """
        orders_response = orders._create_order(base_url=self.base_url, priv_key_wif=priv_key_wif, pair=pair,
                                               blockchain=blockchain, side=side, price=price, want_amount=want_amount,
                                               use_native_tokens=use_native_tokens,
                                               order_type=order_type, contract_hash=contract_hash,
                                               )

        orders_json_resp = response_to_json(orders_response)

        return orders._execute_order(base_url=self.base_url, order=orders_json_resp, priv_key_wif=priv_key_wif,)

    def withdraw(self, priv_key_wif, asset_id, amount, contract_hash, blockchain="NEO"):
        """Withdraw your balanaces from Switcheo smart contract balance.

        This function creates a withdrawal which is later executed.

        To be able to make a withdrawal, sufficient funds are required in the contract balance.
        A signature of the request payload has to be provided for this API call.

        Args:
            priv_key_wif (str)      : The private key wif of the user.
            asset_id (str)          : The asset symbol or ID to withdraw. for eg. SWTH
            amount (int)            : Amount of tokens to withdraw.
            contract_hash (str)     : Switcheo Exchange contract hash to execute the withdraw on.
            blockchain (str)        : Blockchain that the token to withdraw is on. Possible values are: neo.

        Returns:
            An id representing this transaction
            Example response:
            {
              "id": "e0f56e23-2e11-4848-b749-a147c872cbe6"
            }

        """
        withdrawals_response = withdrawals._create_withdrawal(base_url=self.base_url, asset_id=asset_id,
                                                              contract_hash=contract_hash, amount=amount,
                                                              priv_key_wif=priv_key_wif, blockchain=blockchain)
        withdrawals_response_json_obj = response_to_json(withdrawals_response)
        # Now lets execute withdrawal
        return withdrawals._execute_withdrawal(base_url=self.base_url,
                                               withdrawal=withdrawals_response_json_obj,
                                               priv_key_wif=priv_key_wif)

    def create_cancellation(self, order_id, priv_key_wif):
        """This API is responsible for order cancellation.

        Only orders with makes and with an available_amount of more than 0 can be cancelled.

        Args:
            order_id (str) : The order id which needs to be cancelled.
        Returns:
            If response from the server is HTTP_OK (200) then this returns the requests.response object

        """
        cancellation_response = orders._create_cancellation(self.base_url, order_id, priv_key_wif)
        cancellation_resp_json = response_to_json(cancellation_response)
        return orders._execute_cancellation(self.base_url, cancellation_resp_json, priv_key_wif)
