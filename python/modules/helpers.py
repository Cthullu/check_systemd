#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helpers used by various submodules.
"""

__author__: str = "Daniel Kuß"

import subprocess

def runtime_window(unitname: str, timeframe: int) -> bool:
    """
    Check if a systemd timer has run within a given time window.

    :param unitname: str
    :param timeframe: int

    :return: bool
        True: if the specified timer ran within the given time window
        False: if the specified timer did not run within the given time window
    """
    last_execution = subprocess.run(
        ["systemctl", "show", unitname, "--property", "LastTriggerUSec"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )
    last_execution = last_execution.stdout.split("=")[1].strip()

    last_execution_sec = subprocess.run(
        ["date", "--date", f"{last_execution}", "+%s"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )
    last_execution_sec = int(last_execution_sec.stdout.strip())

    next_execution = subprocess.run(
        ["systemctl", "show", unitname, "--property", "NextElapseUSecRealtime"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )
    next_execution = next_execution.stdout.split("=")[1].strip()

    next_execution_sec = subprocess.run(
        ["date", "--date", f"{next_execution}", "+%s"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )
    next_execution_sec = int(next_execution_sec.stdout.strip())

    max_last_execution_sec = subprocess.run(
        ["date", "--date", f"{timeframe} minutes ago", "+%s"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )

    max_next_execution_sec = subprocess.run(
        ["date", "--date", f"{timeframe} minutes", "+%s"],
        check = False,
        capture_output = True,
        encoding = 'utf-8',
    )

    if ((last_execution_sec < int(max_last_execution_sec.stdout)) and
        (next_execution_sec > int(max_next_execution_sec.stdout))):
        ret_val = False
    else:
        ret_val = True

    return ret_val


def check_exists(unitname: str) -> bool:
    """
    Check if a systemd service exists.

    :param unitname: str

    :return: bool
        True: if the specified service exists
        False: if the specified service does not exist
    """
    try:
        subprocess.run(
        ["systemctl", "status", unitname],
        check=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        )
        exists = True
    except subprocess.CalledProcessError:
        exists = False

    return exists


def check_running(unitname: str) -> bool:
    """
    Check if a systemd service is running.

    :param unitname: str

    :return: bool
        True: if the specified service is running
        False: if the specified service is not running
    """
    try:
        subprocess.run(
            ["systemctl", "is-active", unitname],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            )
        running = True
    except subprocess.CalledProcessError:
        running = False

    return running


def check_enabled(unitname: str) -> bool:
    """
    Check if a systemd service is enabled.

    :param unitname: str

    :return: bool
        True: if the specified service is enabled
        False: if the specified service is not enabled
    """
    try:
        subprocess.run(
            ["systemctl", "is-enabled", unitname],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        enabled = True
    except subprocess.CalledProcessError:
        enabled = False

    return enabled


def suffix_check(unitname: str, suffix: str) -> bool:
    """
    Check if the provided unitname has the specified suffix.

    :param unitname: str
    :param suffix: str

    :return: bool
        True: if the unitname has the specified suffix
        False: if the unitname does not have the specified suffix
    """
    return unitname.endswith(suffix)
