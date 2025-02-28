import customtkinter

import os

from core.consts.app_const import AppConst
from core.exceptions.activation_exception import ActivationException
from core.helpers.file_helper import FileHelper
from core.models.option import Option
from core.utility.language import Language
from core.services.pages.video.organization.index_service import IndexService

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

        self.input_sort_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.input_sort_label_var).grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.input_sort_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.input_sort_combobox.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.input_rule_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.input_rule_label_var).grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.input_rule_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.input_rule_combobox.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.client_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.client_label_var).grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.client_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.client_combobox.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

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
        self.input_label_var.set(Language.get("VideoOrganizationIndexPageInputFolder"))
        self.input_button_var.set(Language.get("VideoOrganizationIndexPageInputSelect"))
        self.output_label_var.set(Language.get("VideoOrganizationIndexPageOutputFolder"))
        self.output_button_var.set(Language.get("VideoOrganizationIndexPageOutputSelect"))
        self.input_sort_label_var.set(Language.get("VideoOrganizationIndexPageInputSort"))
        self.input_rule_label_var.set(Language.get("VideoOrganizationIndexPageInputRule"))
        self.client_label_var.set(Language.get("VideoOrganizationIndexPageClient"))
        self.progress_label_var.set(Language.get("VideoOrganizationIndexPageProgress"))
        self.start_button_var.set(Language.get("VideoOrganizationIndexPageStart"))
        self.stop_button_var.set(Language.get("VideoOrganizationIndexPageStop"))

        self.input_sort_source = [
            Option(Language.get("VideoOrganizationIndexPageInputSortName"), "name"),
            Option(Language.get("VideoOrganizationIndexPageInputSortTime"), "time"),
            Option(Language.get("VideoOrganizationIndexPageInputSortSize"), "size"),
        ]
        self.input_sort_combobox.configure(values=Option.get_text_list(self.input_sort_source))

        self.input_rule_source = [
            Option(Language.get("VideoOrganizationIndexPageInputRuleAsc"), "asc"),
            Option(Language.get("VideoOrganizationIndexPageInputRuleDesc"), "desc"),
        ]
        self.input_rule_combobox.configure(values=Option.get_text_list(self.input_rule_source))

        self.client_source = [
            Option(Language.get("VideoOrganizationIndexPageClientBilibiliWindows"), "windows"),
            Option(Language.get("VideoOrganizationIndexPageClientBilibiliAndroid"), "android"),
        ]
        self.client_combobox.configure(values=Option.get_text_list(self.client_source))

        self.file_switch_source = [
            Option(Language.get("VideoOrganizationIndexPageInputFolder"), "input"),
            Option(Language.get("VideoOrganizationIndexPageOutputFolder"), "output"),
        ]
        self.file_switch.configure(values=Option.get_text_list(self.file_switch_source))
        self.file_switch.set(self.file_switch_source[0].text)

        self.add_message(Language.get("VideoOrganizationHelp"), "success")

    def set_show(self):
        self.update()
        self.set_file_grid_view()

    def set_hide(self):
        if self.file_view.video_view:
            self.file_view.stop_video()

    def get_input_sort(self):
        item = Option.get_text_item(self.input_sort_source, self.input_sort_combobox.get())
        return item.value

    def set_input_sort(self, value):
        item = Option.get_value_item(self.input_sort_source, value)
        self.input_sort_combobox.set(item.text)

    def get_input_rule(self):
        item = Option.get_text_item(self.input_rule_source, self.input_rule_combobox.get())
        return item.value

    def set_input_rule(self, value):
        item = Option.get_value_item(self.input_rule_source, value)
        self.input_rule_combobox.set(item.text)

    def get_client(self):
        item = Option.get_text_item(self.client_source, self.client_combobox.get())
        return item.value

    def set_client(self, value):
        item = Option.get_value_item(self.client_source, value)
        self.client_combobox.set(item.text)

    def set_file_view(self):
        path = self.file_grid.get_checked_item()
        if path:
            self.file_view.set_video(path)
        else:
            self.file_view.clear_video()

    def start(self):
        try:
            # self.set_file_switch_grid_view("input")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            input = self.input_entry_var.get()
            if not os.path.isdir(input):
                raise Exception(Language.get("VideoOrganizationIndexPageInputError"))
            output = self.output_entry_var.get()
            if not os.path.isdir(output):
                raise Exception(Language.get("VideoOrganizationIndexPageOutputError"))
            input_files = FileHelper.get_paths(input)
            if not input_files:
                raise Exception(Language.get("VideoOrganizationIndexPageFileError"))
            client = self.get_client()
            if client is None:
                raise Exception(f"{Language.get("VideoOrganizationIndexPageParamError")}: client: {client}")
            self.index_service.start(input, output, input_files, client)
            self.set_file_switch_grid_view("output")
        except ActivationException:
            Validate.license_order_window_show()
        except Exception as e:
            self.add_message(e, "error")
        finally:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.set_progress(0)
