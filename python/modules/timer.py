#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Timer related checks.
"""

__author__: str = "Daniel Kuß"

import logging
from modules import helpers

def main(unitname: str, timeframe: int = 0, logger: logging = None) -> int:
    """
    Main function for timer checks.

    :param unitname: str
    :param timeframe: int
    :param logger: logging

    :return: int
        0: if the specified timer is active (and ran within defined timeframe)
        1: if the specified timer is not active
        1: if the specified timer did not run within defined timeframe
        2: if the specified timer was not found
    """
    logger = logger if logger else logging.getLogger()

    logger.debug("Checking if systemd timer %s exists.", unitname)
    if not helpers.check_exists(unitname):
        logger.error("Timer %s was not found.", unitname)
        return 2

    logger.debug("Checking if systemd timer %s is active.", unitname)
    if not helpers.check_running(unitname):
        logger.error("Timer %s is not active.", unitname)
        return 1

    if timeframe is not None:
        logger.debug("Checking if systemd timer %s ran within the last %d minutes.",
            unitname, timeframe)
        if not helpers.runtime_window(unitname, timeframe):
            logger.error("Timer %s did not run within the last %d minutes.", unitname, timeframe)
            return 1

    return 0
