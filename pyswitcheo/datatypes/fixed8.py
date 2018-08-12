# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implementation for custom datatypes to interact with the blockchain."""
from decimal import Decimal
from pyswitcheo.crypto_utils import reverse_hex

import logging

logger = logging.getLogger(__name__)


class Fixed8(object):
    """Fixed point representation of a given input number."""

    def __init__(self, value):
        """."""
        self.__value = float(Decimal(value).quantize(Decimal("1.00000000")))

    def to_hex(self):
        output = hex(round(self.__value * 1e+8))[2:]
        return "0" * (16 - len(output)) + output

    def to_reverse_hex(self):
        """Get a reverse hex representation of a given Fixed8."""
        return reverse_hex(self.to_hex())

    @property
    def value(self):
        """Return the underlying value of fixed 8."""
        return str(self.__value)

    @staticmethod
    def num_to_fixed_8(number, size=8):
        """Convert a given number to Fixed8 representation.

        Args:
            number (float/int) : Input which needs to be converted to a Fixed8 representation.
        Returns:
            Given number in Fixed8 representation.
        Raises:
            TypeError in case size param is not an integer

        """
        if size % 1 != 0:
            raise TypeError(
                "size param must be a whole integer. Received {size}".format(size=size)
            )
        return Fixed8(number).to_reverse_hex()[: size * 2]
