#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Argument parsers for the check_systemd_service.py and check_systemd_timer.py scripts.
"""

import argparse

def get_parser(version: str) -> argparse.ArgumentParser:
    """
    Returns an ArgumentParser for the check_systemd.py script.

    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog = "check_systemd",
        description="Checksystemd service and timer units.",
    )

    parser.add_argument(
        "-d", "--debug",
        dest = "debug",
        help = "turn on debug logging",
        action = "store_true",
        default = False,
    )

    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = f'%(prog)s {version}'
    )

    subparsers = parser.add_subparsers(
        title = "subcommands",
        description = "valid subcommands",
        help = "additional help",
        dest = "subcommand",
    )

    service_group = subparsers.add_parser(
        name = "service",
        help = "systemd service related checks",
    )

    service_group.add_argument(
        '-s', '--service',
        type = str,
        dest = "service",
        metavar = "<service>",
        help = "the name of the systemd service to check",
        required = True,
    )

    timer_group = subparsers.add_parser(
        name = "timer",
        help = "systemd timer related checks",
    )

    timer_group.add_argument(
        '-t', '--timer',
        type = str,
        dest = "timer",
        metavar = "<timer>",
        help = "the name of the systemd timer to check",
        required = True,
    )

    timer_group.add_argument(
        '-w', '--window',
        type = int,
        dest = "time_window",
        metavar = "<window>",
        help = "the time window in minutes in which the timer should have run",
        required = False,
    )

    return parser
