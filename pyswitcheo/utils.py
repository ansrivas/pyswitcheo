# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities to be used."""

import json
import math
import logging
import datetime
from http import HTTPStatus
from pyswitcheo.errors import HTTPResponseError
from pyswitcheo.internal.api import exchange


logger = logging.getLogger(__name__)


def format_urls(base_url, end_point):
    """Create a url given a base url and an end point.

    Args:
        base_url (str): A base url which needs to be queried.
        end_point(str): The other part of the end point
    Returns:
        A properly formatted url to query
    """
    url = '/'.join([str(base_url).strip('/'), str(end_point).strip('/')])
    logger.debug("Url to query: {0}".format(url))
    return url


def convert_to_neo_asset_amount(amount, asset_id, base_url):
    """Convert a given input to a neo asset precision.

    Internally this API queries the Switcheo exchange to get the correct precision
    for a given asset.

    Args:
        amount (int)   : Input amount for which precision needs to be calculated.
        asset_id (str) : A string representing the correct asset.
        base_url (str) : URL of the switcheo exchange which will return the correct decimal precision.
    """
    # sanitize the asset_id
    asset_id = str(asset_id).lower()
    response = exchange._get_contract_tokens_info(base_url)
    json_resp = response_to_json(response)

    # sanitize the json_response, i.e. all keys should be lower
    json_resp_sanitized = {str(k).lower(): v for k, v in json_resp.items()}
    precision = json_resp_sanitized[asset_id]["decimals"]
    return int(amount * math.pow(10, precision))


def response_else_exception(response):
    """Return a response in case HTTPStatus is 200, else raise a custom exception.
    """
    if response.status_code != HTTPStatus.OK:
        logger.debug("Response returned from the server: {0}".format(response.text))
        raise HTTPResponseError(response)
    return response


def response_to_json(response):
    """A simple wrapper to convert requests.content or requests.text to a corresponding json object."""
    logger.debug("Original response {}".format(response.content.decode("UTF-8")))
    json_response = json.loads(response.content.decode("UTF-8"))
    logger.debug("Response dumped as json {0}".format(json_response))
    return json_response


def jsonify(json_obj):
    """Convert a given json object to string with sorted key and without spaces."""
    logger.debug("Json before invoking jsonify {}".format(json_obj))
    return json.dumps(json_obj, sort_keys=True, separators=(",", ":"))


def get_current_epoch_milli():
    """Get the current time in epoch milliseconds."""
    return int(round(datetime.datetime.now().timestamp() * 1000))
