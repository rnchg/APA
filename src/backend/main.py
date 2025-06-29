import logging
from core.utility.logger import Logger
from services.app_service import AppService


if __name__ == "__main__":
    try:
        Logger.setup()
        AppService().start()
    except Exception as e:
        logging.exception(e)
