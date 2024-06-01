#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check systemd services and timers.
"""

__author__: str = "Daniel Kuß"
__version__: str = "0.1.0"

import logging
import sys
from modules import argument_parser

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

    return 0

if __name__ == "__main__":
    sys.exit(main())
