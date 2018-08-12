# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Withdrawals related URIs"""

# This endpoint creates a withdrawal which can be executed through Execute Withdrawal. To be able to make a
# withdrawal, sufficient funds are required in the contract balance.
CREATE_WITHDRAWAL = "/withdrawals"


# This is the second endpoint required to execute a withdrawal. After using the Create Withdrawal endpoint, you
# will receive a response which requires additional signing.
EXECUTE_WITHDRAWAL = "/withdrawals/{id}/broadcast"
