import customtkinter
import tkinter as tk

from core.consts.app_const import AppConst
from core.utility.current import Current
from core.utility.language import Language

from views.windows.app.main_window import *

from resources.default import Default


class ConfigWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__()

        self.main: MainWindow = master

        self.set_window()
        self.set_icon()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_widgets()
        self.init_data()

        self.init_language()

        self.update()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

    def set_window(self):
        self.center_window(1280, 720)
        self.minsize(960, 640)
        self.grab_set()

    def set_icon(self):
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, Default.Images.app()))

    def init_widgets(self):
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.footer_frame = customtkinter.CTkFrame(self)
        self.footer_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nse")

        self.prompt_system_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.content_frame, textvariable=self.prompt_system_label_var).grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        self.prompt_system_textbox = customtkinter.CTkTextbox(self.content_frame)
        self.prompt_system_textbox.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

        self.prompt_max_length_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.content_frame, textvariable=self.prompt_max_length_label_var).grid(row=2, column=0, padx=10, pady=10, sticky="nsw")
        self.prompt_max_length_entry_var = customtkinter.StringVar()
        customtkinter.CTkEntry(self.content_frame, textvariable=self.prompt_max_length_entry_var).grid(row=3, column=0, padx=10, pady=0, sticky="nsew")

        self.context_max_length_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.content_frame, textvariable=self.context_max_length_label_var).grid(row=4, column=0, padx=10, pady=10, sticky="nsw")
        self.context_max_length_entry_var = customtkinter.StringVar()
        customtkinter.CTkEntry(self.content_frame, textvariable=self.context_max_length_entry_var).grid(row=5, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.save_button_var = customtkinter.StringVar()
        customtkinter.CTkButton(self.footer_frame, textvariable=self.save_button_var, command=self.save_button_command).grid(row=0, column=0, padx=10, pady=0, sticky="nsew")

        self.close_button_var = customtkinter.StringVar()
        customtkinter.CTkButton(self.footer_frame, textvariable=self.close_button_var, fg_color=AppConst.Color.error, command=self.close_button_command).grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

    def init_data(self):
        self.prompt_system_textbox.insert("0.0", Current.config.gen_chat.prompt_system)
        self.prompt_max_length_entry_var.set(Current.config.gen_chat.prompt_max_length)
        self.context_max_length_entry_var.set(Current.config.gen_chat.context_max_length)

    def init_language(self):
        self.title(Language.get("GenChatConfigWindowConfig"))
        self.prompt_system_label_var.set(Language.get("GenChatConfigWindowPromptSystem"))
        self.prompt_max_length_label_var.set(Language.get("GenChatConfigWindowPromptMaxLength"))
        self.context_max_length_label_var.set(Language.get("GenChatConfigWindowContextMaxLength"))
        self.save_button_var.set(Language.get("GenChatConfigWindowSetSave"))
        self.close_button_var.set(Language.get("GenChatConfigWindowSetClose"))

    def set_show(self):
        pass

    def set_hide(self):
        pass

    def save_button_command(self):
        Current.config.gen_chat.prompt_system = self.prompt_system_textbox.get("0.0", tk.END).rstrip()
        Current.config.gen_chat.prompt_max_length = self.prompt_max_length_entry_var.get()
        Current.config.gen_chat.context_max_length = self.context_max_length_entry_var.get()

    def close_button_command(self):
        self.destroy()
