import logging
from spot2ytm.config.settings import settings


class LoggingConfigurator:
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def configure(self):
        level = logging.DEBUG if self.debug else logging.INFO

        logging.basicConfig(
            filename=settings.BASE_DIR / "logs" / "spot2ytm.log",
            filemode='a',
            level=level,
            format="%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        )