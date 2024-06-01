#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checks if a provided systemd service is running and enabled.
"""

__author__: str = "Daniel Kuß"
__version__: str = "0.1.0"

import logging
import sys
from modules import argument_parser, service_checks

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


def main():
    """
    Main function.

    :return: int
        0: if the specified service runs and is enabled
        1: if the specified service runs but is not enables
        2: if the specified service was not found
        2: if the specified service does not run
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname) -8s] (%(filename)s:%(lineno)d) %(message)s",
    )
    logger = logging.getLogger(__name__)

    logger.debug("Parsing command line arguments.")
    cli_args = argument_parser.get_service_parser(__version__)
    cli_args = cli_args.parse_args()

    if cli_args.debug:
        logger.setLevel(level=logging.DEBUG)
        logger.debug("Debug logging enabled.")
    else:
        logging.basicConfig(level=logging.INFO)

    logger.debug("Check if the provided service name has the '.service' suffix.")
    if not suffix_check(cli_args.service, ".service"):
        logger.error("Service name %s does not have the '.service' suffix.", cli_args.service)
        sys.exit(3)

    logger.debug("Checking if systemd service %s exists, is running and enabled.", cli_args.service)
    ret_val = service_checks.check_service_exists(cli_args.service, logger)

    return ret_val


if __name__ == "__main__":
    sys.exit(main())
