import sys
from core.utility.logger import Logger
from core.helpers.file_helper import FileHelper

from services.app_service import AppService


logger = Logger(FileHelper.frozen_executable_path("logs")).logger
sys.stdout = logger
sys.stderr = logger


if __name__ == "__main__":
    try:
        AppService().start()
    except Exception as e:
        logger.error(f"main Exception: {e}", exc_info=True, stack_info=True)
