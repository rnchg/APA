import os

import customtkinter

from core.consts.app_const import AppConst
from core.consts.audio_const import AudioConst
from core.exceptions.activation_exception import ActivationException
from core.models.option import Option
from core.helpers.file_helper import FileHelper
from core.utility.language import Language
from core.services.pages.audio.stt.index_service import IndexService

from domain.adapters.windows.adapter import Adapter
from domain.views.base.base_page import BasePage
from domain.utility.validate import Validate


class IndexPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            input_exts=AppConst.audio_exts,
            output_exts=AppConst.text_exts,
            **kwargs,
        )

    def init_widgets(self):
        super().init_widgets()

        self.provider_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.provider_label_var).grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.provider_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.provider_combobox.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.mode_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.mode_label_var).grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.mode_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.mode_combobox.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.option_frame = customtkinter.CTkFrame(self.header_frame)
        self.option_frame.grid(row=4, column=0, columnspan=3, padx=0, pady=0, sticky="nsew")
        self.option_frame.grid_columnconfigure(1, weight=1)

        self.language_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.option_frame, textvariable=self.language_label_var).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.language_combobox = customtkinter.CTkOptionMenu(self.option_frame, state="readonly")
        self.language_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.similarity_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.option_frame, textvariable=self.similarity_label_var).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.similarity_slider = customtkinter.CTkSlider(self.option_frame, from_=0, to=1)
        self.similarity_slider.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        self.message_textbox = customtkinter.CTkTextbox(self.run_message_frame, width=360)
        self.message_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def init_data(self):
        self.index_service = IndexService()
        self.index_service.get_stop = self.get_stop
        self.index_service.set_progress = self.set_progress
        self.index_service.add_message = self.add_message

    def init_language(self):
        self.input_label_var.set(Language.get("AudioSTTIndexPageInputFolder"))
        self.input_button_var.set(Language.get("AudioSTTIndexPageInputSelect"))
        self.output_label_var.set(Language.get("AudioSTTIndexPageOutputFolder"))
        self.output_button_var.set(Language.get("AudioSTTIndexPageOutputSelect"))
        self.provider_label_var.set(Language.get("AudioSTTIndexPageProvider"))
        self.mode_label_var.set(Language.get("AudioSTTIndexPageMode"))
        self.language_label_var.set(Language.get("AudioSTTIndexPageLanguage"))
        self.similarity_label_var.set(Language.get("AudioSTTIndexPageSimilarity"))
        self.progress_label_var.set(Language.get("AudioSTTIndexPageProgress"))
        self.start_button_var.set(Language.get("AudioSTTIndexPageStart"))
        self.stop_button_var.set(Language.get("AudioSTTIndexPageStop"))

        self.provider_source = Adapter.providers
        self.provider_combobox.configure(values=Option.get_text_list(self.provider_source))

        self.mode_source = [
            Option(Language.get("AudioSTTIndexPageModeStandard"), "standard"),
        ]
        self.mode_combobox.configure(values=Option.get_text_list(self.mode_source))

        self.language_source = [
            Option(Language.get("AudioSTTIndexPageLanguageAuto"), 0),
            Option(Language.get("AudioSTTIndexPageLanguageZh"), 1),
            Option(Language.get("AudioSTTIndexPageLanguageEn"), 2),
            Option(Language.get("AudioSTTIndexPageLanguageYue"), 3),
            Option(Language.get("AudioSTTIndexPageLanguageJa"), 4),
            Option(Language.get("AudioSTTIndexPageLanguageKo"), 5),
        ]
        self.language_combobox.configure(values=Option.get_text_list(self.language_source))

        self.file_switch_source = [
            Option(Language.get("AudioSTTIndexPageInputFolder"), "input"),
            Option(Language.get("AudioSTTIndexPageOutputFolder"), "output"),
        ]
        self.file_switch.configure(values=Option.get_text_list(self.file_switch_source))
        self.file_switch.set(self.file_switch_source[0].text)

        self.add_message(Language.get("AudioSTTHelp"), "success")

    def set_show(self):
        self.update()
        self.set_file_grid_view()

    def set_hide(self):
        if self.file_view.audio_view:
            self.file_view.stop_audio()

    def get_provider(self):
        item = Option.get_text_item(self.provider_source, self.provider_combobox.get())
        return item.value

    def set_provider(self, value):
        item = Option.get_value_item(self.provider_source, value)
        self.provider_combobox.set(item.text)

    def get_mode(self):
        item = Option.get_text_item(self.mode_source, self.mode_combobox.get())
        return item.value

    def set_mode(self, value):
        item = Option.get_value_item(self.mode_source, value)
        self.mode_combobox.set(item.text)

    def get_language(self):
        item = Option.get_text_item(self.language_source, self.language_combobox.get())
        return item.value

    def set_language(self, value):
        item = Option.get_value_item(self.language_source, value)
        self.language_combobox.set(item.text)

    def get_similarity(self):
        return self.similarity_slider.get()

    def set_similarity(self, value):
        self.similarity_slider.set(value)

    def set_file_view(self):
        path = self.file_grid.get_checked_item()
        if path:
            if os.path.splitext(path)[-1].lower() in AppConst.text_exts:
                self.file_view.set_image_view_visible(False)
                self.file_view.set_audio_control_visible(False)
                self.file_view.set_text_view_visible(True)
                self.file_view.set_text(path)
            elif os.path.splitext(path)[-1].lower() in AppConst.audio_exts:
                self.file_view.set_image_view_visible(True)
                self.file_view.set_audio_control_visible(True)
                self.file_view.set_text_view_visible(False)
                self.file_view.set_audio(path)
        else:
            if self.file_view.text_visible:
                self.file_view.clear_text()
            elif self.file_view.audio_visible:
                self.file_view.clear_audio()

    def start(self):
        try:
            self.set_file_switch_grid_view("input")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            input = self.input_entry_var.get()
            if not os.path.isdir(input):
                raise Exception(Language.get("AudioSTTIndexPageInputError"))
            output = self.output_entry_var.get()
            if not os.path.isdir(output):
                raise Exception(Language.get("AudioSTTIndexPageOutputError"))
            input_files = self.file_grid.get_file_path()
            if not input_files:
                raise Exception(Language.get("AudioSTTIndexPageFileError"))
            provider = self.get_provider()
            if provider is None:
                raise Exception(f"{Language.get("AudioSTTIndexPageParamError")}: provider: {provider}")
            mode = self.get_mode()
            if mode is None:
                raise Exception(f"{Language.get("AudioSTTIndexPageParamError")}: mode: {mode}")
            language = self.get_language()
            if language is None:
                raise Exception(f"{Language.get("AudioSTTIndexPageParamError")}: language: {language}")
            similarity = self.get_similarity()
            if similarity is None:
                raise Exception(f"{Language.get("AudioSTTIndexPageParamError")}: similarity: {similarity}")
            self.index_service.start(input, output, input_files, provider, mode, language, similarity)
            self.set_file_switch_grid_view("output")
        except ActivationException:
            Validate.license_order_window_show()
        except Exception as e:
            self.add_message(e, "error")
        finally:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.set_progress(0)
