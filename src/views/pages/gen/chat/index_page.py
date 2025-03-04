import customtkinter
import threading

from core.consts.app_const import AppConst
from core.consts.gen_const import GenConst
from core.exceptions.activation_exception import ActivationException
from core.exceptions.process_stop_exception import ProcessStopException
from core.utility.current import Current
from core.utility.language import Language
from core.services.pages.gen.chat.index_service import IndexService

from domain.widgets.chat_view.view import View as ChatView
from domain.widgets.chat_view.model import Model as ChatModel
from domain.utility.validate import Validate

from views.windows.app.main_window import *


class IndexPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.main: MainWindow = master

        self.is_init = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_widgets()
        self.init_data()

        self.init_language()

    def init_widgets(self):
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.footer_frame = customtkinter.CTkFrame(self)
        self.footer_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.gen_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.content_frame, textvariable=self.gen_label_var).grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.gen_view = ChatView(self.content_frame)
        self.gen_view.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.prompt_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.footer_frame, textvariable=self.prompt_label_var).grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.message_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.footer_frame, textvariable=self.message_label_var).grid(row=0, column=1, padx=10, pady=10, sticky="nse")

        self.message_textbox = customtkinter.CTkTextbox(self.footer_frame, height=120)
        self.message_textbox.grid(row=1, rowspan=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.message_textbox.bind("<KeyRelease>", self.message_textbox_key_release)
        self.message_textbox.bind("<Control-Return>", self.message_textbox_control_return)

        self.send_button_var = customtkinter.StringVar()
        self.send_button = customtkinter.CTkButton(self.footer_frame, textvariable=self.send_button_var, command=lambda: self.send_button_command(), width=60, fg_color=AppConst.Color.info)
        self.send_button.grid(row=1, column=2, padx=10, pady=10, sticky="sew")

        self.cancel_button_var = customtkinter.StringVar()
        customtkinter.CTkButton(self.footer_frame, textvariable=self.cancel_button_var, command=self.cancel_button_command, width=60, fg_color=AppConst.Color.warning).grid(row=1, column=3, padx=10, pady=10, sticky="sew")

        self.reset_button_var = customtkinter.StringVar()
        customtkinter.CTkButton(self.footer_frame, textvariable=self.reset_button_var, command=self.reset_button_command, width=60, fg_color=AppConst.Color.error).grid(row=2, column=2, padx=10, pady=10, sticky="new")

        self.config_button_var = customtkinter.StringVar()
        customtkinter.CTkButton(self.footer_frame, textvariable=self.config_button_var, command=self.config_button_command, width=60, fg_color=AppConst.Color.success).grid(row=2, column=3, padx=10, pady=10, sticky="new")

    def init_data(self):
        self.set_message()
        self.index_service = IndexService()

    def init_language(self):
        self.gen_label_var.set(Language.get("GenChatIndexPageHistory"))
        self.send_button_var.set(Language.get("GenChatIndexPageSend"))
        self.cancel_button_var.set(Language.get("GenChatIndexPageCancel"))
        self.reset_button_var.set(Language.get("GenChatIndexPageReset"))
        self.config_button_var.set(Language.get("GenChatIndexPageConfig"))
        self.gen_view.add_model(ChatModel(type=GenConst.Chat.type_system, text=f"{Language.get("GenChatHelp")}"))

    def set_show(self):
        self.update()
        self.after(100, threading.Thread(target=self.init).start())

    def set_hide(self):
        pass

    def get_prompt(self):
        return self.message_textbox.get("0.0", "end").rstrip()

    def clear_prompt(self):
        self.message_textbox.delete("0.0", "end")

    def set_message(self):
        self.prompt = self.get_prompt()
        self.message = f"{Language.get("GenChatIndexPageMessage")} [ {len(self.prompt)}/{Current.config.gen_chat.prompt_max_length} ]"
        self.message_label_var.set(self.message)

    def message_textbox_key_release(self, event):
        if not self.is_init:
            return
        self.set_message()

    def message_textbox_control_return(self, event):
        if not self.is_init:
            return
        self.send_button_command()

    def send_button_command(self):
        if not self.is_init:
            return
        threading.Thread(target=self.send).start()

    def cancel_button_command(self):
        if not self.is_init:
            return
        self.index_service.cancel.set()
        self.gen_view.set_cancel()
        self.prompt_label_var.set(Language.get("GenChatIndexPageInputPrompt"))

    def reset_button_command(self):
        if not self.is_init:
            return
        self.cancel_button_command()
        self.gen_view.set_clear()

    def config_button_command(self):
        if not self.is_init:
            return
        self.main.gen_chat_config_setting_window_show()

    def init(self):
        if self.is_init:
            return
        try:
            self.prompt_label_var.set(Language.get("GenChatIndexPageModelInitWait"))
            self.send_button.configure(state="disabled")
            self.update()
            self.index_service.init()
            self.index_service.token = self.get_token
            self.prompt_label_var.set(Language.get("GenChatIndexPageInputPrompt"))
            self.send_button.configure(state="normal")
            self.is_init = True
        except Exception as e:
            self.prompt_label_var.set(Language.get("GenChatIndexPageModelInitFailed"))

    def send(self):
        try:
            if self.send_button.cget("state") == "disabled":
                return
            self.prompt = self.get_prompt()
            if not self.prompt:
                return
            self.send_button.configure(state="disabled")
            self.prompt_label_var.set(Language.get("GenChatIndexPageModelProcessWait"))
            self.index_service.cancel.clear()
            self.clear_prompt()
            self.prompt, self.assistant = self.gen_view.send_and_build_model(ChatModel(type=GenConst.Chat.type_user, text=self.prompt))
            self.index_service.start(self.prompt)
            self.prompt_label_var.set(Language.get("GenChatIndexPageInputPrompt"))
        except ActivationException:
            Validate.license_order_window_show()
            self.gen_view.set_cancel()
            self.clear_prompt()
        except ProcessStopException:
            self.clear_prompt()
        except Exception as e:
            self.clear_prompt()
            self.prompt_label_var.set(e)
        finally:
            self.send_button.configure(state="normal")

    def get_token(self, token):
        self.assistant.textbox.insert("end", token)
        self.gen_view.update_item(self.assistant)
