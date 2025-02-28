import customtkinter

from core.models.option import Option
from core.utility.current import Current
from core.utility.language import Language

from domain.widgets.card.card import Card
from domain.utility.validate import Validate

from views.windows.app.main_window import *

from resources.default import Default


class SettingPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.main: MainWindow = master

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_widgets()
        self.init_data()

        self.init_language()

    def init_widgets(self):
        self.header_frame = customtkinter.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.theme_frame = customtkinter.CTkFrame(self.header_frame)
        self.theme_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.theme_frame.grid_columnconfigure(0, weight=1)

        self.language_frame = customtkinter.CTkFrame(self.header_frame)
        self.language_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.language_frame.grid_columnconfigure(0, weight=1)

        self.mode_frame = customtkinter.CTkFrame(self.header_frame)
        self.mode_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.mode_frame.grid_columnconfigure(0, weight=1)

        self.gen_chat_frame = customtkinter.CTkFrame(self.header_frame)
        self.gen_chat_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.gen_chat_frame.grid_columnconfigure(0, weight=1)

        self.license_frame = customtkinter.CTkFrame(self.header_frame)
        self.license_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.license_frame.grid_columnconfigure(0, weight=1)

        self.theme_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.theme_frame, textvariable=self.theme_label_var, image=Default.Images.theme, compound="left").grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.theme_combobox = customtkinter.CTkOptionMenu(self.theme_frame, state="readonly", command=self.theme_combobox_command)
        self.theme_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="nse")

        self.language_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.language_frame, textvariable=self.language_label_var, image=Default.Images.language, compound="left").grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.language_combobox = customtkinter.CTkOptionMenu(self.language_frame, state="readonly", command=self.language_combobox_command)
        self.language_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="nse")

        self.mode_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.mode_frame, textvariable=self.mode_label_var, image=Default.Images.mode, compound="left").grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.mode_combobox = customtkinter.CTkOptionMenu(self.mode_frame, state="readonly", command=self.mode_combobox_command)
        self.mode_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="nse")

        self.gen_chat_config_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.gen_chat_frame, textvariable=self.gen_chat_config_label_var, image=Default.Images.gen_chat, compound="left").grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.gen_chat_config_setting_button_var = customtkinter.StringVar()
        self.gen_chat_config_setting_button = customtkinter.CTkButton(self.gen_chat_frame, textvariable=self.gen_chat_config_setting_button_var, command=self.gen_chat_config_setting_button_command)
        self.gen_chat_config_setting_button.grid(row=0, column=1, padx=10, pady=10, sticky="nse")

        self.license_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.license_frame, textvariable=self.license_label_var, image=Default.Images.license, compound="left").grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.license_info_button_var = customtkinter.StringVar()
        self.license_info_button = customtkinter.CTkButton(self.license_frame, textvariable=self.license_info_button_var, command=self.license_info_button_command)
        self.license_info_button.grid(row=0, column=1, padx=10, pady=10, sticky="nse")

        self.license_order_button_var = customtkinter.StringVar()
        self.license_order_button = customtkinter.CTkButton(self.license_frame, textvariable=self.license_order_button_var, command=self.license_order_button_command)
        self.license_order_button.grid(row=0, column=2, padx=10, pady=10, sticky="nse")

        self.about_card_var = customtkinter.StringVar()
        Card(self.content_frame, textvariable=self.about_card_var, image=Default.Images.logo).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        Card(self.content_frame, text="Email: Rnchg@Hotmail.com").grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        Card(self.content_frame, text="Github: github.com/rnchg/apa").grid(row=2, column=0, padx=10, pady=0, sticky="nsew")
        Card(self.content_frame, text="Gitee: gitee.com/rnchg/apa").grid(row=3, column=0, padx=10, pady=0, sticky="nsew")
        Card(self.content_frame, text="Youtube: Light Cloud Wind").grid(row=4, column=0, padx=10, pady=0, sticky="nsew")
        Card(self.content_frame, text="Bilibili: 风轻云也净").grid(row=5, column=0, padx=10, pady=0, sticky="nsew")
        Card(self.content_frame, text="QQ: 6085398").grid(row=6, column=0, padx=10, pady=0, sticky="nsew")

    def init_data(self):
        pass

    def init_language(self):
        self.theme_label_var.set(Language.get("SettingPageTheme"))
        self.language_label_var.set(Language.get("SettingPageLanguage"))
        self.mode_label_var.set(Language.get("SettingPageMode"))
        self.gen_chat_config_label_var.set(Language.get("SettingPageGenChatConfig"))
        self.gen_chat_config_setting_button_var.set(Language.get("SettingPageGenChatConfigSetting"))
        self.license_label_var.set(Language.get("SettingPageLicense"))
        self.license_info_button_var.set(Language.get("SettingPageLicenseInfo"))
        self.license_order_button_var.set(Language.get("SettingPageLicenseOrder"))
        self.about_card_var.set(f"  {Language.get("ApplicationTitle")}")

        self.theme_source = [
            Option(Language.get("SettingPageThemeSystem"), "system"),
            Option(Language.get("SettingPageThemeLight"), "light"),
            Option(Language.get("SettingPageThemeDark"), "dark"),
        ]
        self.theme_combobox.configure(values=Option.get_text_list(self.theme_source))

        self.language_source = Language.get_options()
        self.language_combobox.configure(values=Option.get_text_list(self.language_source))

        self.mode_source = [
            Option(Language.get("SettingPageModeBalanced"), "balanced"),
            Option(Language.get("SettingPageModePerformance"), "performance"),
        ]
        self.mode_combobox.configure(values=Option.get_text_list(self.mode_source))

        self.set_theme(Current.config.setting.theme)
        self.set_language(Current.config.setting.language)
        self.set_mode(Current.config.setting.mode)

    def set_theme(self, value):
        item = Option.get_value_item(self.theme_source, value)
        self.theme_combobox.set(item.text)
        customtkinter.set_appearance_mode(value)

    def set_language(self, value):
        self.language_combobox.set(value)

    def set_mode(self, value):
        item = Option.get_value_item(self.mode_source, value)
        self.mode_combobox.set(item.text)

    def theme_combobox_command(self, text):
        item = Option.get_text_item(self.theme_source, text)
        Current.config.setting.theme = item.value
        customtkinter.set_appearance_mode(item.value)

    def language_combobox_command(self, text):
        Current.config.setting.language = text
        Language.update(text)
        self.main.set_language()
        self.main.service.get_config()

    def mode_combobox_command(self, text):
        item = Option.get_text_item(self.mode_source, text)
        Current.config.setting.mode = item.value

    def gen_chat_config_setting_button_command(self):
        self.main.gen_chat_config_setting_window_show()

    def license_info_button_command(self):
        Validate.license_info_window_show()

    def license_order_button_command(self):
        Validate.license_order_window_show()
