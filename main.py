from ytmusicapi import YTMusic, OAuthCredentials
from dotenv import load_dotenv
import os
from spot2ytm.config.settings import settings
from spot2ytm.config.logging_config import LoggingConfigurator


load_dotenv()

def main():
    LoggingConfigurator(settings.DEBUG).configure()


if __name__ == '__main__':
    main()