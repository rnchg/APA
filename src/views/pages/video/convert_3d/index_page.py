import customtkinter

import os

from core.consts.app_const import AppConst
from core.exceptions.activation_exception import ActivationException
from core.models.option import Option
from core.utility.language import Language
from core.services.pages.video.convert_3d.index_service import IndexService

from domain.adapters.windows.adapter import Adapter
from domain.views.base.base_page import BasePage
from domain.utility.validate import Validate


class IndexPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            input_exts=AppConst.video_exts,
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

        self.format_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.option_frame, textvariable=self.format_label_var).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.format_combobox = customtkinter.CTkOptionMenu(self.option_frame, state="readonly")
        self.format_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.shift_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.option_frame, textvariable=self.shift_label_var).grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.shift_combobox = customtkinter.CTkOptionMenu(self.option_frame, state="readonly")
        self.shift_combobox.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.pop_out_label_var = customtkinter.StringVar()
        self.pop_out_var = customtkinter.StringVar()
        self.pop_out_switch = customtkinter.CTkSwitch(self.option_frame, textvariable=self.pop_out_label_var, variable=self.pop_out_var, onvalue="on", offvalue="off")
        self.pop_out_switch.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        self.cross_eye_label_var = customtkinter.StringVar()
        self.cross_eye_var = customtkinter.StringVar()
        self.cross_eye_switch = customtkinter.CTkSwitch(self.option_frame, textvariable=self.cross_eye_label_var, variable=self.cross_eye_var, onvalue="on", offvalue="off")
        self.cross_eye_switch.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")

        self.message_textbox = customtkinter.CTkTextbox(self.run_message_frame, width=360)
        self.message_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.file_view.set_image_view_visible(True)
        self.file_view.set_video_control_visible(True)

    def init_data(self):
        self.index_service = IndexService()
        self.index_service.get_stop = self.get_stop
        self.index_service.set_progress = self.set_progress
        self.index_service.add_message = self.add_message

    def init_language(self):
        self.input_label_var.set(Language.get("VideoConvert3dIndexPageInputFolder"))
        self.input_button_var.set(Language.get("VideoConvert3dIndexPageInputSelect"))
        self.output_label_var.set(Language.get("VideoConvert3dIndexPageOutputFolder"))
        self.output_button_var.set(Language.get("VideoConvert3dIndexPageOutputSelect"))
        self.provider_label_var.set(Language.get("VideoConvert3dIndexPageProvider"))
        self.mode_label_var.set(Language.get("VideoConvert3dIndexPageMode"))
        self.format_label_var.set(Language.get("VideoConvert3dIndexPageFormat"))
        self.shift_label_var.set(Language.get("VideoConvert3dIndexPageShift"))
        self.pop_out_label_var.set(Language.get("VideoConvert3dIndexPagePopOut"))
        self.cross_eye_label_var.set(Language.get("VideoConvert3dIndexPageCrossEye"))
        self.progress_label_var.set(Language.get("VideoConvert3dIndexPageProgress"))
        self.start_button_var.set(Language.get("VideoConvert3dIndexPageStart"))
        self.stop_button_var.set(Language.get("VideoConvert3dIndexPageStop"))

        self.provider_source = Adapter.providers
        self.provider_combobox.configure(values=Option.get_text_list(self.provider_source))

        self.mode_source = [
            Option(Language.get("VideoConvert3dIndexPageModeStandard"), "standard"),
        ]
        self.mode_combobox.configure(values=Option.get_text_list(self.mode_source))

        self.format_source = [
            Option(Language.get("VideoConvert3dIndexPageFormatHalfSbs"), "half_sbs"),
            Option(Language.get("VideoConvert3dIndexPageFormatSbs"), "sbs"),
            Option(Language.get("VideoConvert3dIndexPageFormatAnaglyph"), "anaglyph"),
            Option(Language.get("VideoConvert3dIndexPageFormatDepth"), "depth"),
        ]
        self.format_combobox.configure(values=Option.get_text_list(self.format_source))

        self.shift_source = [
            Option(Language.get("VideoConvert3dIndexPageShift10"), 10),
            Option(Language.get("VideoConvert3dIndexPageShift20"), 20),
            Option(Language.get("VideoConvert3dIndexPageShift30"), 30),
            Option(Language.get("VideoConvert3dIndexPageShift50"), 50),
            Option(Language.get("VideoConvert3dIndexPageShift100"), 100),
            Option(Language.get("VideoConvert3dIndexPageShift200"), 200),
            Option(Language.get("VideoConvert3dIndexPageShift300"), 300),
            Option(Language.get("VideoConvert3dIndexPageShift500"), 500),
            Option(Language.get("VideoConvert3dIndexPageShift1000"), 1000),
        ]
        self.shift_combobox.configure(values=Option.get_text_list(self.shift_source))

        self.file_switch_source = [
            Option(Language.get("VideoConvert3dIndexPageInputFolder"), "input"),
            Option(Language.get("VideoConvert3dIndexPageOutputFolder"), "output"),
        ]
        self.file_switch.configure(values=Option.get_text_list(self.file_switch_source))
        self.file_switch.set(self.file_switch_source[0].text)

        self.add_message(Language.get("VideoConvert3dHelp"), "success")

    def set_show(self):
        self.update()
        self.set_file_grid_view()

    def set_hide(self):
        if self.file_view.video_view:
            self.file_view.stop_video()

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

    def get_format(self):
        item = Option.get_text_item(self.format_source, self.format_combobox.get())
        return item.value

    def set_format(self, value):
        item = Option.get_value_item(self.format_source, value)
        self.format_combobox.set(item.text)

    def get_shift(self):
        item = Option.get_text_item(self.shift_source, self.shift_combobox.get())
        return item.value

    def set_shift(self, value):
        item = Option.get_value_item(self.shift_source, value)
        self.shift_combobox.set(item.text)

    def get_pop_out(self):
        return self.pop_out_var.get()

    def set_pop_out(self, value):
        self.pop_out_var.set(value)

    def get_cross_eye(self):
        return self.cross_eye_var.get()

    def set_cross_eye(self, value):
        self.cross_eye_var.set(value)

    def set_file_view(self):
        path = self.file_grid.get_checked_item()
        if path:
            self.file_view.set_video(path)
        else:
            self.file_view.clear_video()

    def start(self):
        try:
            self.set_file_switch_grid_view("input")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            input = self.input_entry_var.get()
            if not os.path.isdir(input):
                raise Exception(Language.get("VideoConvert3dIndexPageInputError"))
            output = self.output_entry_var.get()
            if not os.path.isdir(output):
                raise Exception(Language.get("VideoConvert3dIndexPageOutputError"))
            input_files = self.file_grid.get_file_path()
            if not input_files:
                raise Exception(Language.get("VideoConvert3dIndexPageFileError"))
            provider = self.get_provider()
            if provider is None:
                raise Exception(f"{Language.get("VideoConvert3dIndexPageParamError")}: provider: {provider}")
            mode = self.get_mode()
            if mode is None:
                raise Exception(f"{Language.get("VideoConvert3dIndexPageParamError")}: mode: {mode}")
            format = self.get_format()
            if format is None:
                raise Exception(f"{Language.get("VideoConvert3dIndexPageParamError")}: format: {format}")
            shift = self.get_shift()
            if shift is None:
                raise Exception(f"{Language.get("VideoConvert3dIndexPageParamError")}: shift: {shift}")
            pop_out = self.get_pop_out()
            if pop_out is None:
                raise Exception(f"{Language.get("VideoConvert3dIndexPageParamError")}: pop_out: {pop_out}")
            cross_eye = self.get_cross_eye()
            if cross_eye is None:
                raise Exception(f"{Language.get("VideoConvert3dIndexPageParamError")}: cross_eye: {cross_eye}")
            self.index_service.start(input, output, input_files, provider, mode, format, shift, pop_out, cross_eye)
            self.set_file_switch_grid_view("output")
        except ActivationException:
            Validate.license_order_window_show()
        except Exception as e:
            self.add_message(e, "error")
        finally:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.set_progress(0)
