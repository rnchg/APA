import webview
from core.utility.logger import Logger
from services.app_service import AppService


if __name__ == "__main__":
    try:
        Logger.setup()
        AppService().start()
    except Exception:
        webview.logger.error(f"Main Exception", exc_info=True)
