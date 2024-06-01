#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service related checks.
"""

__author__: str = "Daniel Kuß"

import logging
from modules import helpers

def main(unitname: str, logger: logging = None) -> int:
    """
    Main function for service checks.

    :param unitname: str
    :param logger: logging

    :return: int
        0: if the specified service runs and is enabled
        1: if the specified service runs but is not enables
        2: if the specified service was not found
        2: if the specified service does not run
    """
    logger = logger if logger else logging.getLogger()

    logger.debug("Checking if systemd service %s exists.", unitname)
    if not helpers.check_exists(unitname):
        logger.debug("Service %s was not found.", unitname)
        return 2

    logger.debug("Checking if systemd service %s is running.", unitname)
    if not helpers.check_running(unitname):
        logger.debug("Service %s does not run.", unitname)
        return 2

    logger.debug("Checking if systemd service %s is enabled.", unitname)
    if not helpers.check_enabled(unitname):
        logger.debug("Service %s is not enabled.", unitname)
        return 1

    return 0
