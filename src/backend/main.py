import sys
from core.utility.logger import Logger
from core.helpers.file_helper import FileHelper

from services.app_host_service import AppHostService


logger = Logger(FileHelper.frozen_executable_path("logs")).log


def app_run():
    try:
        logger.info("Start")
        AppHostService().start()
        logger.info("Stop")
    except Exception as e:
        logger.error("Exception", e)


if __name__ == "__main__":
    sys.stdout = logger
    sys.stderr = logger
    app_run()
