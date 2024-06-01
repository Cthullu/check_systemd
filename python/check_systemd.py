#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check systemd services and timers.
"""

__author__: str = "Daniel Kuß"
__version__: str = "0.1.0"
__src__: str = "https://github.com/Cthullu/check_systemd"

import logging
import sys
from modules import argument_parser, service, timer, helpers

def main() -> int:
    """
    Main function.

    :return: int
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname) -8s] (%(filename)s:%(lineno)d) %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.debug("Parsing command line arguments.")
    cli_args = argument_parser.get_parser(__version__).parse_args()

    if cli_args.debug:
        logger.setLevel(level=logging.DEBUG)
        logger.debug("Debug logging enabled.")
    else:
        logging.basicConfig(level=logging.INFO)

    if cli_args.subcommand is None:
        logger.error("No subcommand provided.")
        return 3

    if cli_args.subcommand == "service":
        logger.debug("Checking systemd service: %s", cli_args.service)
        if not helpers.suffix_check(cli_args.service, ".service"):
            logger.error("Service name %s does not have the '.service' suffix.", cli_args.service)
            return 3

        return service.main(cli_args.service, logger)

    if cli_args.subcommand == "timer":
        logger.debug("Checking systemd timer: %s", cli_args.timer)
        if not helpers.suffix_check(cli_args.timer, ".timer"):
            logger.error("Timer name %s does not have the '.timer' suffix.", cli_args.timer)
            return 3

        return timer.main(cli_args.timer, cli_args.time_window, logger)

    logger.debug("I do not know how I ended here, so I just exit clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
