import os

import customtkinter

from core.consts.app_const import AppConst
from core.consts.audio_const import AudioConst
from core.exceptions.activation_exception import ActivationException
from core.models.option import Option
from core.helpers.file_helper import FileHelper
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

        self.option_frame = customtkinter.CTkFrame(self.header_frame)
        self.option_frame.grid(row=4, column=0, columnspan=3, padx=0, pady=0, sticky="nsew")
        self.option_frame.grid_columnconfigure(1, weight=1)

        self.clone_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.option_frame, textvariable=self.clone_label_var).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.clone_combobox = customtkinter.CTkOptionMenu(self.option_frame, state="readonly")
        self.clone_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.clone_config_button_var = customtkinter.StringVar()
        self.clone_config_button = customtkinter.CTkButton(self.option_frame, textvariable=self.clone_config_button_var, width=60, command=self.clone_config_button_command)
        self.clone_config_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.clone_update_button_var = customtkinter.StringVar()
        self.clone_update_button = customtkinter.CTkButton(self.option_frame, textvariable=self.clone_update_button_var, width=60, command=self.clone_update_button_command)
        self.clone_update_button.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

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
        self.clone_label_var.set(Language.get("AudioTTSIndexPageClone"))
        self.clone_config_button_var.set(Language.get("AudioTTSIndexPageCloneConfig"))
        self.clone_update_button_var.set(Language.get("AudioTTSIndexPageCloneUpdate"))
        self.progress_label_var.set(Language.get("AudioTTSIndexPageProgress"))
        self.start_button_var.set(Language.get("AudioTTSIndexPageStart"))
        self.stop_button_var.set(Language.get("AudioTTSIndexPageStop"))

        self.provider_source = Adapter.providers
        self.provider_combobox.configure(values=Option.get_text_list(self.provider_source))

        self.mode_source = [
            Option(Language.get("AudioTTSIndexPageModeStandard"), "standard"),
        ]
        self.mode_combobox.configure(values=Option.get_text_list(self.mode_source))

        self.update_clones()

        self.file_switch_source = [
            Option(Language.get("AudioTTSIndexPageInputFolder"), "input"),
            Option(Language.get("AudioTTSIndexPageOutputFolder"), "output"),
        ]
        self.file_switch.configure(values=Option.get_text_list(self.file_switch_source))
        self.file_switch.set(self.file_switch_source[0].text)

        self.add_message(Language.get("AudioTTSHelp"), "success")

    def get_clones(self):
        result = []
        audios = FileHelper.get_paths(AudioConst.TTS.model_clone_dir, AppConst.audio_exts)
        for audio in audios:
            dir = os.path.dirname(audio)
            base = os.path.basename(audio)
            name = os.path.splitext(base)[0]
            text = os.path.join(dir, f"{name}.txt")
            if os.path.isfile(text):
                result.append(Option(base, (audio, text)))
        return result

    def update_clones(self):
        self.clone_source = self.get_clones()
        if not self.clone_source:
            return
        self.clone_combobox.configure(values=Option.get_text_list(self.clone_source))
        self.clone_combobox.set(self.clone_source[0].text)

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

    def get_clone(self):
        item = Option.get_text_item(self.clone_source, self.clone_combobox.get())
        return item.value

    def set_clone(self, value):
        item = Option.get_value_item(self.clone_source, value)
        self.clone_combobox.set(item.text)

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
            clone = self.get_clone()
            if clone is None:
                raise Exception(f"{Language.get("AudioTTSIndexPageParamError")}: clone: {clone}")
            self.index_service.start(input, output, input_files, provider, mode, clone)
            self.set_file_switch_grid_view("output")
        except ActivationException:
            Validate.license_order_window_show()
        except Exception as e:
            self.add_message(e, "error")
        finally:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.set_progress(0)

    def clone_config_button_command(self):
        try:
            os.startfile(os.path.abspath(AudioConst.TTS.model_clone_dir))
        except Exception as e:
            self.add_message(e, "error")

    def clone_update_button_command(self):
        self.update_clones()
