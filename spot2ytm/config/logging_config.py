"""Logging configuration setup.

This module provides configuration for the application's logging system, setting up
file-based logging with appropriate formatting and log levels.
"""

import logging
from spot2ytm.config.settings import settings


class LoggingConfigurator:
    """Configures application logging settings.
    
    Sets up file-based logging with appropriate formatting and dynamically adjusts
    the logging level based on debug mode.
    """
    
    def __init__(self, debug: bool = False) -> None:
        """Initialize the logging configurator.
        \n        Args:
            debug: If True, sets logging level to DEBUG; otherwise INFO.
        """
        self.debug = debug

    def configure(self):
        """Configure the logging system.
        \n        Sets up file-based logging to 'logs/spot2ytm.log' with timestamps,
        log levels, module names, and formatted messages.
        """
        level = logging.DEBUG if self.debug else logging.INFO

        logging.basicConfig(
            filename=settings.BASE_DIR / "logs" / "spot2ytm.log",
            filemode='a',
            level=level,
            format="%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        )