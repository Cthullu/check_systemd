#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check if a systemd timer exists and is acitve.
If in addition a time-window is provided, the script will check if the timer had run within given
window.
"""

__author__: str = "Daniel Kuß"
__version__: str = "0.1.0"

import logging
import sys
from modules import argument_parser, timer_checks

def main():
    """
    Main function.

    :return: int
        0: if the specified timer is active and did run within the defined timeframe
        1: if the specified timer is not active
        1: if the specified timer did not run within defined timeframe
        2: if the specified timer was not found
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname) -8s] (%(filename)s:%(lineno)d) %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.debug("Parsing command line arguments.")
    cli_args = argument_parser.get_timer_parser(__version__)
    cli_args = cli_args.parse_args()

    if cli_args.debug:
        logger.setLevel(level=logging.DEBUG)
        logger.debug("Debug logging enabled.")
    else:
        logging.basicConfig(level=logging.INFO)

    logger.debug("Checking if systemd timer %s exists and is enabled.", cli_args.timer)
    ret_val_status = timer_checks.check_timer_status(cli_args.timer, logger)

    if cli_args.time_window:
        logger.debug("Checking if systemd timer %s runs within specified time window %s.",
            cli_args.timer,
            cli_args.time_window
        )
        ret_val_timer = timer_checks.check_runtime_window(
            cli_args.timer,
            cli_args.time_window,
            logger
        )
    else:
        logger.debug("No time window specified. Skipping runtime check.")
        ret_val_timer = 0

    ret_val = max(ret_val_status, ret_val_timer)

    return ret_val


if __name__ == "__main__":
    sys.exit(main())
