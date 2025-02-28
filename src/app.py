from tkinter import messagebox
from services.app_host_service import AppHostService


def app_run():
    try:
        AppHostService().start()
    except Exception as e:
        messagebox.showerror("Exception", e)


if __name__ == "__main__":
    app_run()
