"""
This file contains the logging configuration for the project.
"""

import logging

from rich.console import Console
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

console = Console()
log = logging.getLogger("rich")


def set_log_level(verbosity: int):
    if verbosity == 0:
        log.setLevel(logging.CRITICAL)
    elif verbosity == 1:
        log.setLevel(logging.ERROR)
    if verbosity == 2:
        log.setLevel(logging.WARNING)
    elif verbosity == 3:
        log.setLevel(logging.INFO)
    elif verbosity == 4:
        log.setLevel(logging.DEBUG)
    return log
