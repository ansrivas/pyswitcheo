# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module can be used to validate incoming response from Switcheo API server."""


LIST_TRADES_SCHEMA = {
    "type": "array",
    "properties": {
        "id": {"type": "string"},
        "fill_amount": {"type": "number"},
        "take_amount": {"type": "number"},
        "is_buy": {"type": "boolean"},
    },
}

# Sample schema for the response expected from execute_withdrawal end point
EXECUTE_WITHDRAWAL_SCHEMA = {
    "type": "object",
    "properties": {
        "event_type": {"type": "string"},
        "amount": {"type": "number"},
        "asset_id": {"type": "string"},
        "status": {"type": "string"},
        "id": {"type": "string"},
        "blockchain": {"type": "string"},
        "reason_code": {"type": "number"},
        "address": {"type": "string"},
        "transaction_hash": {"type": "object"},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
        "contract_hash": {"type": "string"},
    },
}
# Sample schema for the response expected from create_withdrawal end point
CREATE_WITHDRAWAL_SCHEMA = {"type": "object", "properties": {"id": {"type": "string"}}}

# Sample schema for the response expected from create_deposit end point
CREATE_DEPOSIT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "transaction": {
            "type": "object",
            "properties": {
                "hash": {"type": "string"},
                "sha256": {"type": "string"},
                "type": {"type": "number"},
                "version": {"type": "number"},
                "attributes": {"type": "array"},
                "inputs": {"type": "array"},
                "outputs": {"type": "array"},
                "scripts": {"type": "array"},
                "script": {"type": "string"},
                "gas": {"type": "number"},
            },
        },
        "script_params": {
            "type": "object",
            "properties": {
                "scriptHash": {"type": "string"},
                "operation": {"type": "string"},
                "args": {"type": "array"},
            },
        },
    },
}


# This is the response received after creating an order
CREATE_ORDER_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "blockchain": {"type": "string"},
        "contract_hash": {"type": "string"},
        "address": {"type": "string"},
        "side": {"type": "string"},
        "offer_asset_id": {"type": "string"},
        "want_asset_id": {"type": "string"},
        "offer_amount": {"type": "string"},
        "want_amount": {"type": "string"},
        "transfer_amount": {"type": "string"},
        "priority_gas_amount": {"type": "string"},
        "use_native_token": {"type": "boolean"},
        "native_fee_transfer_amount": {"type": "number"},
        "deposit_txn": {"type": ["object", "null"]},
        "created_at": {"type": "string"},
        "status": {"type": "string"},
        "fills": {"type": "array"},
        "makes": {"type": "array"},
    },
}
