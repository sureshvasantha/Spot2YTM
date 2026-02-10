from spot2ytm.config.settings import settings
from spot2ytm.config.logging_config import LoggingConfigurator
from spot2ytm.app import create_app


def main():
    LoggingConfigurator(settings.DEBUG).configure()
    migrator = create_app()

    migrator.migrate(
        spotify_playlist_id=settings.MY_PL_ID
    )


if __name__ == "__main__":
    main()