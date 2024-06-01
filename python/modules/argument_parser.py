#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Argument parsers for the check_systemd_service.py and check_systemd_timer.py scripts.
"""

import argparse

def get_service_parser(version):
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
        help = "turn on debug logging",
        action = "store_true",
        default = False,
    )

    parser.add_argument(
       "-s", "--service",
        type = str,
        metavar = "<service>",
        help = "the name of the systemd service to check",
        required = True,
    )

    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = f'%(prog)s {version}'
    )

    return parser.parse_args()
