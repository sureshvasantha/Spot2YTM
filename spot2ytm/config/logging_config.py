import logging


class LoggingConfigurator:
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def configure(self):
        level = logging.DEBUG if self.debug else logging.INFO

        logging.basicConfig(
            level=level,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )