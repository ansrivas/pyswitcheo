# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implementation for custom datatypes to interact with the blockchain."""

from collections import namedtuple

# Represents a TransactionAttribute
TransactionAttribute = namedtuple("TransactionAttribute", ["usage", "data"])

# Represents a TransactionInput
TransactionInput = namedtuple("TransactionInput", ["prevHash", "prevIndex"])

# Represents a TransactionOutput
TransactionOutput = namedtuple("TransactionOutput", ["assetId", "value", "scriptHash"])

# Represents a Witness
Witness = namedtuple("Witness", ["invocationScript", "verificationScript"])
