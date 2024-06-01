#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checks to determine if a systemd service exists, runs and is enabled.
"""

__author__: str = "Daniel Kuß"

import logging
import subprocess

def check_service_exists(service: str, logger: logging = None) -> int:
    """
    Check if a systemd service exists, runs and is enabled.

    :param service: str
    :param logger: logging

    :return: int
        0: if the specified service runs and is enabled
        1: if the specified service runs but is not enables
        2: if the specified service was not found
        2: if the specified service does not run
    """

    logger = logger if logger else logging.getLogger()

    logger.debug("Checking if systemd service %s exists.", service)
    try:
        subprocess.run(
        ["systemctl", "status", service],
        check=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        logger.debug("Service %s was not found.", service)
        return 2

    logger.debug("Checking if systemd service %s is running.", service)
    try:
        subprocess.run(
            ["systemctl", "is-active", service],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            )
    except subprocess.CalledProcessError:
        logger.debug("Service %s does not run.", service)
        return 2

    logger.debug("Checking if systemd service %s is enabled.", service)
    try:
        subprocess.run(
            ["systemctl", "is-enabled", service],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        logger.debug("Service %s is not enabled.", service)
        return 1

    return 0
