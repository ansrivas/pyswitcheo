# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deposits related end points to be used on Switcheo."""

# This endpoint creates a deposit which can be executed through Execute Deposit. To be able to make a deposit,
# sufficient funds are required in the depositing wallet
CREATE_DEPOSIT = "/deposits"


# This is the second endpoint required to execute a deposit.
EXECUTE_DEPOSIT = "/deposits/{id}/broadcast"
