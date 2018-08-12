# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to contracts end points"""

from http import HTTPStatus
from pyswitcheo.internal.api import contracts
from pyswitcheo.utils import response_to_json


def test_list_contracts(url):
    """Test list contracts end points."""
    response = contracts._list_contracts(url.testnet)

    assert response.status_code == HTTPStatus.OK

    # Assuming NEO will always be in the deployed contracts.
    json_response = response_to_json(response)
    assert "NEO" in list(json_response.keys())
