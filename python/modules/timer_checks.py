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
    last_execution = subprocess.run(
        ["systemctl", "show", timer, "--property", "LastTriggerUSec"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )

    last_execution = last_execution.stdout.split("=")[1].strip()

    logger.debug("Convert last execution timestamp %s to seconds.", last_execution)
    last_execution_sec = subprocess.run(
        ["date", "--date", f"{last_execution}", "+%s"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )

    last_execution_sec = int(last_execution_sec.stdout.strip())

    logger.debug("Get timestamp of next run of systemd timer %s.", timer)
    next_execution = subprocess.run(
        ["systemctl", "show", timer, "--property", "NextElapseUSecRealtime"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )

    next_execution = next_execution.stdout.split("=")[1].strip()

    logger.debug("Convert next execution timestamp %s to seconds.", last_execution)
    next_execution_sec = subprocess.run(
        ["date", "--date", f"{next_execution}", "+%s"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )

    next_execution_sec = int(next_execution_sec.stdout.strip())

    logger.debug("Calculate timestamps for time window %s.", time_window)
    max_last_execution_sec = subprocess.run(
        ["date", "--date", f"{time_window} minutes ago", "+%s"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )

    max_next_execution_sec = subprocess.run(
        ["date", "--date", f"{time_window} minutes", "+%s"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )

    logger.debug("Compare timestamps.")
    if (last_execution_sec < int(max_last_execution_sec.stdout)) and (next_execution_sec > int(max_next_execution_sec.stdout)):
        logger.debug("Timer %s will not run in specified timeframe.", timer)
        return 1

    return 0
