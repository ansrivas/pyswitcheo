# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Orders are instructions to buy or sell assets on Switcheo Exchange."""

# Retrieves orders from a specific address filtered by the given parameters.
LIST_ORDERS = "/orders"

# This endpoint creates an order which can be executed through Broadcast Order.
CREATE_ORDER = "/orders"

# This is the second endpoint required to execute an order. After using the Create Order endpoint,
# you will receive a response which needs to be signed.
EXECUTE_ORDER = "/orders/{id}/broadcast"

# This is the first API call required to cancel an order.
CREATE_CANCELLATION = "/cancellations"

# This is the second endpoint that must be called to cancel an order. After calling the Create Cancellation
# endpoint, you will receive a transaction in the response which must be signed.
EXECUTE_CANCELLATION = "/cancellations/{id}/broadcast"
