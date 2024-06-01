#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Argument parsers for the check_systemd_service.py and check_systemd_timer.py scripts.
"""

import argparse

def get_service_parser(version: str) -> argparse.ArgumentParser:
    """
    Returns an ArgumentParser for the check_systemd_service.py script.

    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog = "check_systemd_service",
        description="Check if a systemd service is running and enabled.",
    )

    parser.add_argument(
        "-d", "--debug",
        type = bool,
        dest = "debug",
        help = "turn on debug logging",
        action = "store_true",
        default = False,
    )

    parser.add_argument(
       "-s", "--service",
        type = str,
        dest = "service",
        metavar = "<service>",
        help = "the name of the systemd service to check",
        required = True,
    )

    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = f'%(prog)s {version}'
    )

    return parser


def get_timer_parser(version: str) -> argparse.ArgumentParser:
    """
    Returns an ArgumentParser for the check_systemd_timer.py script.

    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog = "check_systemd_timer",
        description="Check if a systemd timer is active and optionally if it ran within a given "
            "time window.",
    )

    parser.add_argument(
        "-d", "--debug",
        type = bool,
        dest = "debug",
        help = "turn on debug logging",
        action = "store_true",
        default = False,
    )

    parser.add_argument(
        "-t", "--timer",
        type = str,
        dest = "timer",
        metavar = "<timer>",
        help = "the name of the systemd timer to check",
        required = True,
    )

    parser.add_argument(
        "-w", "--window",
        type = int,
        dest = "time_window",
        metavar = "<window>",
        help = "the time window in seconds in which the timer should have run",
        required = False,
    )

    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = f'%(prog)s {version}'
    )

    return parser
