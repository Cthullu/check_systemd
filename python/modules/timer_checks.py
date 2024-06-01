#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checks to determine if a systemd timer exists, is enabled and runs within a given timeframe.
"""

__author__: str = "Daniel Kuß"

import logging
import subprocess

def check_timer_status(timer: str, logger: logging = None) -> int:
    """
    Check if a systemd timer exists, and is active.

    :param service: str
    :param logger: logging

    :return: int
        0: if the specified timer is active
        1: if the specified timer is not active
        2: if the specified timer was not found
    """

    logger = logger if logger else logging.getLogger()

    logger.debug("Checking if systemd timer %s exists.", timer)
    try:
        subprocess.run(
            ["systemctl", "status", timer],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        logger.debug("Timer %s was not found.", timer)
        return 2

    logger.debug("Checking if systemd timer %s is active.", timer)
    try:
        subprocess.run(
            ["systemctl", "is-active", timer],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        logger.debug("Timer %s is not active.", timer)
        return 1

    return 0

def check_runtime_window(timer: str, time_window: int, logger: logging = None) -> int:
    """
    Check if a systemd timer has run within a given time window.

    :param timer: str
    :param time_window: int
    :param logger: logging

    :return: int
        0: if the specified timer ran within the given time window
        1: if the specified timer did not run within the given time window
    """

    logger = logger if logger else logging.getLogger()

    logger.debug("Checking if systemd timer %s ran within the given time window %s.",
        timer, time_window)

    logger.debug("Get timestamp of last run of systemd timer %s.", timer)
    # LAST_EXECUTION=$(systemctl show "${SYSTEMD_TIMER}" --property LastTriggerUSec --value)
    last_execution = subprocess.run(
        ["systemctl", "show", timer, "--property", "LastTriggerUSec"],
        check = False
    )

    # LAST_EXECUTION_SEC=$(date --date "${LAST_EXECUTION}" +'%s')

    logger.debug("Get timestamo of next run of systemd timer %s.", timer)
    # NEXT_EXECUTION=$(systemctl show "${SYSTEMD_TIMER}" --property NextElapseUSecRealtime --value)
    next_execution = subprocess.run(
        ["systemctl", "show", timer, "--property", "NextElapseUSecRealtime"],
        check = False,
    )

    # NEXT_EXECUTION_SEC=$(date --date "${NEXT_EXECUTION}" +'%s')'

    logger.debug("Calculate timestamps for time window %s.", time_window)
    # MAX_LAST_EXECUTION_SEC=$(date --date "${TIMEFRAME} minutes ago" +'%s')
    # MAX_NEXT_EXECUTION_SEC=$(date --date "${TIMEFRAME} minutes" +'%s')

    logger.debug("Compare timestamps.")
    # if [[ ${LAST_EXECUTION_SEC} -lt ${MAX_LAST_EXECUTION_SEC} ]] && [[ ${NEXT_EXECUTION_SEC} -gt ${MAX_NEXT_EXECUTION_SEC} ]]; then
    # echo "Warning: ${SYSTEMD_TIMER} will not run in specified timeframe "
    # exit 1

    return 0
