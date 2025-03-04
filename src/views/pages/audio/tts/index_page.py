import os

import customtkinter

from core.consts.app_const import AppConst
from core.exceptions.activation_exception import ActivationException
from core.models.option import Option
from core.utility.language import Language
from core.services.pages.audio.tts.index_service import IndexService

from domain.adapters.windows.adapter import Adapter
from domain.views.base.base_page import BasePage
from domain.utility.validate import Validate


class IndexPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            input_exts=AppConst.text_exts,
            output_exts=AppConst.audio_exts,
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

        self.voice_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.voice_label_var).grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.voice_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.voice_combobox.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.message_textbox = customtkinter.CTkTextbox(self.run_message_frame, width=360)
        self.message_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def init_data(self):
        self.index_service = IndexService()
        self.index_service.get_stop = self.get_stop
        self.index_service.set_progress = self.set_progress
        self.index_service.add_message = self.add_message

    def init_language(self):
        self.input_label_var.set(Language.get("AudioTTSIndexPageInputFolder"))
        self.input_button_var.set(Language.get("AudioTTSIndexPageInputSelect"))
        self.output_label_var.set(Language.get("AudioTTSIndexPageOutputFolder"))
        self.output_button_var.set(Language.get("AudioTTSIndexPageOutputSelect"))
        self.provider_label_var.set(Language.get("AudioTTSIndexPageProvider"))
        self.mode_label_var.set(Language.get("AudioTTSIndexPageMode"))
        self.voice_label_var.set(Language.get("AudioTTSIndexPageVoice"))
        self.progress_label_var.set(Language.get("AudioTTSIndexPageProgress"))
        self.start_button_var.set(Language.get("AudioTTSIndexPageStart"))
        self.stop_button_var.set(Language.get("AudioTTSIndexPageStop"))

        self.provider_source = Adapter.providers
        self.provider_combobox.configure(values=Option.get_text_list(self.provider_source))

        self.mode_source = [
            Option(Language.get("AudioTTSIndexPageModeStandard"), "standard"),
        ]
        self.mode_combobox.configure(values=Option.get_text_list(self.mode_source))

        self.voice_source = [
            Option(f"{Language.get("AudioTTSIndexPageVoiceEnFemale")} [ af_maple ]", "af_maple"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceEnFemale")} [ af_sol ]", "af_sol"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceEnFemale")} [ bf_vale ]", "bf_vale"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_001 ]", "zf_001"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_002 ]", "zf_002"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_003 ]", "zf_003"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_004 ]", "zf_004"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_005 ]", "zf_005"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_006 ]", "zf_006"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_007 ]", "zf_007"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_008 ]", "zf_008"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_017 ]", "zf_017"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhFemale")} [ zf_018 ]", "zf_018"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_009 ]", "zm_009"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_010 ]", "zm_010"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_011 ]", "zm_011"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_012 ]", "zm_012"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_013 ]", "zm_013"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_014 ]", "zm_014"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_015 ]", "zm_015"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_016 ]", "zm_016"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_020 ]", "zm_020"),
            Option(f"{Language.get("AudioTTSIndexPageVoiceZhMale")} [ zm_025 ]", "zm_025"),
        ]
        self.voice_combobox.configure(values=Option.get_text_list(self.voice_source))

        self.file_switch_source = [
            Option(Language.get("AudioTTSIndexPageInputFolder"), "input"),
            Option(Language.get("AudioTTSIndexPageOutputFolder"), "output"),
        ]
        self.file_switch.configure(values=Option.get_text_list(self.file_switch_source))
        self.file_switch.set(self.file_switch_source[0].text)

        self.add_message(Language.get("AudioTTSHelp"), "success")

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

    def get_voice(self):
        item = Option.get_text_item(self.voice_source, self.voice_combobox.get())
        return item.value

    def set_voice(self, value):
        item = Option.get_value_item(self.voice_source, value)
        self.voice_combobox.set(item.text)

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
                raise Exception(Language.get("AudioTTSIndexPageInputError"))
            output = self.output_entry_var.get()
            if not os.path.isdir(output):
                raise Exception(Language.get("AudioTTSIndexPageOutputError"))
            input_files = self.file_grid.get_file_path()
            if not input_files:
                raise Exception(Language.get("AudioTTSIndexPageFileError"))
            provider = self.get_provider()
            if provider is None:
                raise Exception(f"{Language.get("AudioTTSIndexPageParamError")}: provider: {provider}")
            mode = self.get_mode()
            if mode is None:
                raise Exception(f"{Language.get("AudioTTSIndexPageParamError")}: mode: {mode}")
            voice = self.get_voice()
            if voice is None:
                raise Exception(f"{Language.get("AudioTTSIndexPageParamError")}: voice: {voice}")
            self.index_service.start(input, output, input_files, provider, mode, voice)
            self.set_file_switch_grid_view("output")
        except ActivationException:
            Validate.license_order_window_show()
        except Exception as e:
            self.add_message(e, "error")
        finally:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.set_progress(0)
