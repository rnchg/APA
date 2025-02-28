import customtkinter
from tkinter import messagebox

from core.utility.language import Language

from domain.widgets.menu.menu import Menu

import views.windows.gen.chat.config_window as GenChatConfigWindow

import views.pages.app.dashboard_page as AppDashboard
import views.pages.app.setting_page as AppSetting

import views.pages.gen.chat.index_page as GenChat

import views.pages.image.super_resolution.index_page as ImageSuperResolution
import views.pages.image.auto_wipe.index_page as ImageAutoWipe
import views.pages.image.cartoon_comic.index_page as ImageCartoonComic
import views.pages.image.convert_3d.index_page as ImageConvert3d
import views.pages.image.color_restoration.index_page as ImageColorRestoration
import views.pages.image.frame_interpolation.index_page as ImageFrameInterpolation
import views.pages.image.matting.index_page as ImageMatting
import views.pages.image.face_restoration.index_page as ImageFaceRestoration

import views.pages.video.super_resolution.index_page as VideoSuperResolution
import views.pages.video.auto_wipe.index_page as VideoAutoWipe
import views.pages.video.cartoon_comic.index_page as VideoCartoonComic
import views.pages.video.convert_3d.index_page as VideoConvert3d
import views.pages.video.color_restoration.index_page as VideoColorRestoration
import views.pages.video.frame_interpolation.index_page as VideoFrameInterpolation
import views.pages.video.matting.index_page as VideoMatting
import views.pages.video.organization.index_page as VideoOrganization

import views.pages.audio.vocal_split.index_page as AudioVocalSplit
import views.pages.audio.denoise.index_page as AudioDenoise
import views.pages.audio.tts.index_page as AudioTTS
import views.pages.audio.stt.index_page as AudioSTT

from services.app_host_service import *

from resources.default import Default


class MainWindow(customtkinter.CTk):
    def __init__(self, service):
        super().__init__()

        self.service: AppHostService = service

        self.set_window()
        self.set_icon()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.init_menu()
        self.init_widgets()
        self.init_data()

        self.init_language()

    def maximize_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = screen_width - 16
        height = screen_height - 74
        self.geometry(f"{width}x{height}+{0}+{0}")

    def set_window(self):
        self.maximize_window()
        self.minsize(960, 640)
        self.protocol("WM_DELETE_WINDOW", self.set_closing)

    def set_closing(self):
        if messagebox.askokcancel(Language.get("MainWindowHelp"), Language.get("MainWindowExitConfirm")):
            self.service.stop()
            self.destroy()

    def set_icon(self):
        self.wm_iconbitmap()
        self.iconphoto(False, Default.Images.app())

    def init_menu(self):
        self.menu_frame = customtkinter.CTkScrollableFrame(self)
        self.menu_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.menu_frame.grid_rowconfigure(6, weight=1)

        self.logo_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.menu_frame, textvariable=self.logo_label_var, image=Default.Images.logo, anchor="w", compound="left", font=customtkinter.CTkFont(size=12, weight="bold"), width=200).grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.home_menu_var = customtkinter.StringVar()
        self.home_menu = Menu(self.menu_frame, textvariable=self.home_menu_var, image=Default.Images.home, command=lambda: self.set_page("home"))
        self.home_menu.grid(row=1, column=0, sticky="nsew")

        self.gen_frame = customtkinter.CTkFrame(self.menu_frame)
        self.gen_frame.grid(row=2, column=0, sticky="nsew")
        self.gen_frame.grid_columnconfigure(0, weight=1)

        self.image_frame = customtkinter.CTkFrame(self.menu_frame)
        self.image_frame.grid(row=3, column=0, sticky="nsew")
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.video_frame = customtkinter.CTkFrame(self.menu_frame)
        self.video_frame.grid(row=4, column=0, sticky="nsew")
        self.video_frame.grid_columnconfigure(0, weight=1)

        self.audio_frame = customtkinter.CTkFrame(self.menu_frame)
        self.audio_frame.grid(row=5, column=0, sticky="nsew")
        self.audio_frame.grid_columnconfigure(0, weight=1)

        self.setting_menu_var = customtkinter.StringVar()
        self.setting_menu = Menu(self.menu_frame, textvariable=self.setting_menu_var, image=Default.Images.setting, command=lambda: self.set_page("setting"))
        self.setting_menu.grid(row=6, column=0, sticky="sew")

        self.gen_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(master=self.gen_frame, textvariable=self.gen_label_var, image=Default.Images.arrow_down, anchor="w", compound="right", padx=10, pady=10).grid(row=0, column=0, sticky="nsew")

        self.gen_chat_menu_var = customtkinter.StringVar()
        self.gen_chat_menu = Menu(self.gen_frame, textvariable=self.gen_chat_menu_var, image=Default.Images.gen_chat, command=lambda: self.set_page("gen_chat"))
        self.gen_chat_menu.grid(row=1, column=0, sticky="nsew")

        self.image_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(master=self.image_frame, textvariable=self.image_label_var, image=Default.Images.arrow_down, anchor="w", compound="right", padx=10, pady=10).grid(row=0, column=0, sticky="nsew")

        self.image_super_resolution_menu_var = customtkinter.StringVar()
        self.image_super_resolution_menu = Menu(self.image_frame, textvariable=self.image_super_resolution_menu_var, image=Default.Images.image_super_resolution, command=lambda: self.set_page("image_super_resolution"))
        self.image_super_resolution_menu.grid(row=1, column=0, sticky="nsew")

        self.image_auto_wipe_menu_var = customtkinter.StringVar()
        self.image_auto_wipe_menu = Menu(self.image_frame, textvariable=self.image_auto_wipe_menu_var, image=Default.Images.image_auto_wipe, command=lambda: self.set_page("image_auto_wipe"))
        self.image_auto_wipe_menu.grid(row=2, column=0, sticky="nsew")

        self.image_cartoon_comic_menu_var = customtkinter.StringVar()
        self.image_cartoon_comic_menu = Menu(self.image_frame, textvariable=self.image_cartoon_comic_menu_var, image=Default.Images.image_cartoon_comic, command=lambda: self.set_page("image_cartoon_comic"))
        self.image_cartoon_comic_menu.grid(row=3, column=0, sticky="nsew")

        self.image_convert_3d_menu_var = customtkinter.StringVar()
        self.image_convert_3d_menu = Menu(self.image_frame, textvariable=self.image_convert_3d_menu_var, image=Default.Images.image_convert_3d, command=lambda: self.set_page("image_convert_3d"))
        self.image_convert_3d_menu.grid(row=4, column=0, sticky="nsew")

        self.image_color_restoration_menu_var = customtkinter.StringVar()
        self.image_color_restoration_menu = Menu(self.image_frame, textvariable=self.image_color_restoration_menu_var, image=Default.Images.image_color_restoration, command=lambda: self.set_page("image_color_restoration"))
        self.image_color_restoration_menu.grid(row=5, column=0, sticky="nsew")

        self.image_frame_interpolation_menu_var = customtkinter.StringVar()
        self.image_frame_interpolation_menu = Menu(self.image_frame, textvariable=self.image_frame_interpolation_menu_var, image=Default.Images.image_frame_interpolation, command=lambda: self.set_page("image_frame_interpolation"))
        self.image_frame_interpolation_menu.grid(row=6, column=0, sticky="nsew")

        self.image_matting_menu_var = customtkinter.StringVar()
        self.image_matting_menu = Menu(self.image_frame, textvariable=self.image_matting_menu_var, image=Default.Images.image_matting, command=lambda: self.set_page("image_matting"))
        self.image_matting_menu.grid(row=7, column=0, sticky="nsew")

        self.image_face_restoration_menu_var = customtkinter.StringVar()
        self.image_face_restoration_menu = Menu(self.image_frame, textvariable=self.image_face_restoration_menu_var, image=Default.Images.image_face_restoration, command=lambda: self.set_page("image_face_restoration"))
        self.image_face_restoration_menu.grid(row=8, column=0, sticky="nsew")

        self.video_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(master=self.video_frame, textvariable=self.video_label_var, image=Default.Images.arrow_down, anchor="w", compound="right", padx=10, pady=10).grid(row=0, column=0, sticky="nsew")

        self.video_super_resolution_menu_var = customtkinter.StringVar()
        self.video_super_resolution_menu = Menu(self.video_frame, textvariable=self.video_super_resolution_menu_var, image=Default.Images.video_super_resolution, command=lambda: self.set_page("video_super_resolution"))
        self.video_super_resolution_menu.grid(row=1, column=0, sticky="nsew")

        self.video_auto_wipe_menu_var = customtkinter.StringVar()
        self.video_auto_wipe_menu = Menu(self.video_frame, textvariable=self.video_auto_wipe_menu_var, image=Default.Images.video_auto_wipe, command=lambda: self.set_page("video_auto_wipe"))
        self.video_auto_wipe_menu.grid(row=2, column=0, sticky="nsew")

        self.video_cartoon_comic_menu_var = customtkinter.StringVar()
        self.video_cartoon_comic_menu = Menu(self.video_frame, textvariable=self.video_cartoon_comic_menu_var, image=Default.Images.video_cartoon_comic, command=lambda: self.set_page("video_cartoon_comic"))
        self.video_cartoon_comic_menu.grid(row=3, column=0, sticky="nsew")

        self.video_convert_3d_menu_var = customtkinter.StringVar()
        self.video_convert_3d_menu = Menu(self.video_frame, textvariable=self.video_convert_3d_menu_var, image=Default.Images.video_convert_3d, command=lambda: self.set_page("video_convert_3d"))
        self.video_convert_3d_menu.grid(row=4, column=0, sticky="nsew")

        self.video_color_restoration_menu_var = customtkinter.StringVar()
        self.video_color_restoration_menu = Menu(self.video_frame, textvariable=self.video_color_restoration_menu_var, image=Default.Images.video_color_restoration, command=lambda: self.set_page("video_color_restoration"))
        self.video_color_restoration_menu.grid(row=5, column=0, sticky="nsew")

        self.video_frame_interpolation_menu_var = customtkinter.StringVar()
        self.video_frame_interpolation_menu = Menu(self.video_frame, textvariable=self.video_frame_interpolation_menu_var, image=Default.Images.video_frame_interpolation, command=lambda: self.set_page("video_frame_interpolation"))
        self.video_frame_interpolation_menu.grid(row=6, column=0, sticky="nsew")

        self.video_matting_menu_var = customtkinter.StringVar()
        self.video_matting_menu = Menu(self.video_frame, textvariable=self.video_matting_menu_var, image=Default.Images.video_matting, command=lambda: self.set_page("video_matting"))
        self.video_matting_menu.grid(row=7, column=0, sticky="nsew")

        self.video_organization_menu_var = customtkinter.StringVar()
        self.video_organization_menu = Menu(self.video_frame, textvariable=self.video_organization_menu_var, image=Default.Images.video_organization, command=lambda: self.set_page("video_organization"))
        self.video_organization_menu.grid(row=8, column=0, sticky="nsew")

        self.audio_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(master=self.audio_frame, textvariable=self.audio_label_var, image=Default.Images.arrow_down, anchor="w", compound="right", padx=10, pady=10).grid(row=0, column=0, sticky="nsew")

        self.audio_vocal_split_menu_var = customtkinter.StringVar()
        self.audio_vocal_split_menu = Menu(self.audio_frame, textvariable=self.audio_vocal_split_menu_var, image=Default.Images.audio_vocal_split, command=lambda: self.set_page("audio_vocal_split"))
        self.audio_vocal_split_menu.grid(row=1, column=0, sticky="nsew")

        self.audio_denoise_menu_var = customtkinter.StringVar()
        self.audio_denoise_menu = Menu(self.audio_frame, textvariable=self.audio_denoise_menu_var, image=Default.Images.audio_denoise, command=lambda: self.set_page("audio_denoise"))
        self.audio_denoise_menu.grid(row=2, column=0, sticky="nsew")

        self.audio_tts_menu_var = customtkinter.StringVar()
        self.audio_tts_menu = Menu(self.audio_frame, textvariable=self.audio_tts_menu_var, image=Default.Images.audio_tts, command=lambda: self.set_page("audio_tts"))
        self.audio_tts_menu.grid(row=3, column=0, sticky="nsew")

        self.audio_stt_menu_var = customtkinter.StringVar()
        self.audio_stt_menu = Menu(self.audio_frame, textvariable=self.audio_stt_menu_var, image=Default.Images.audio_stt, command=lambda: self.set_page("audio_stt"))
        self.audio_stt_menu.grid(row=4, column=0, sticky="nsew")

    def init_widgets(self):
        self.home_page = AppDashboard.DashboardPage(master=self)

        self.gen_chat_page = GenChat.IndexPage(master=self)

        self.image_super_resolution_page = ImageSuperResolution.IndexPage(master=self)
        self.image_auto_wipe_page = ImageAutoWipe.IndexPage(master=self)
        self.image_cartoon_comic_page = ImageCartoonComic.IndexPage(master=self)
        self.image_convert_3d_page = ImageConvert3d.IndexPage(master=self)
        self.image_color_restoration_page = ImageColorRestoration.IndexPage(master=self)
        self.image_frame_interpolation_page = ImageFrameInterpolation.IndexPage(master=self)
        self.image_matting_page = ImageMatting.IndexPage(master=self)
        self.image_face_restoration_page = ImageFaceRestoration.IndexPage(master=self)

        self.video_super_resolution_page = VideoSuperResolution.IndexPage(master=self)
        self.video_auto_wipe_page = VideoAutoWipe.IndexPage(master=self)
        self.video_cartoon_comic_page = VideoCartoonComic.IndexPage(master=self)
        self.video_convert_3d_page = VideoConvert3d.IndexPage(master=self)
        self.video_color_restoration_page = VideoColorRestoration.IndexPage(master=self)
        self.video_frame_interpolation_page = VideoFrameInterpolation.IndexPage(master=self)
        self.video_matting_page = VideoMatting.IndexPage(master=self)
        self.video_organization_page = VideoOrganization.IndexPage(master=self)

        self.audio_vocal_split_page = AudioVocalSplit.IndexPage(master=self)
        self.audio_denoise_page = AudioDenoise.IndexPage(master=self)
        self.audio_tts_page = AudioTTS.IndexPage(master=self)
        self.audio_stt_page = AudioSTT.IndexPage(master=self)

        self.setting_page = AppSetting.SettingPage(master=self)

        self.gen_chat_config_setting_window = None

    def init_data(self):
        self.set_page("home")

    def init_language(self):
        self.title(Language.get("ApplicationTitle"))
        self.logo_label_var.set(f" {Language.get("ApplicationTitle")}")

        self.home_menu_var.set(Language.get("MainWindowHome"))

        self.gen_label_var.set(Language.get("MainWindowGen"))
        self.gen_chat_menu_var.set(Language.get("MainWindowGenChat"))

        self.image_label_var.set(Language.get("MainWindowImage"))
        self.image_super_resolution_menu_var.set(Language.get("MainWindowImageSuperResolution"))
        self.image_auto_wipe_menu_var.set(Language.get("MainWindowImageAutoWipe"))
        self.image_cartoon_comic_menu_var.set(Language.get("MainWindowImageCartoonComic"))
        self.image_convert_3d_menu_var.set(Language.get("MainWindowImageConvert3d"))
        self.image_color_restoration_menu_var.set(Language.get("MainWindowImageColorRestoration"))
        self.image_frame_interpolation_menu_var.set(Language.get("MainWindowImageFrameInterpolation"))
        self.image_matting_menu_var.set(Language.get("MainWindowImageMatting"))
        self.image_face_restoration_menu_var.set(Language.get("MainWindowImageFaceRestoration"))

        self.video_label_var.set(Language.get("MainWindowVideo"))
        self.video_super_resolution_menu_var.set(Language.get("MainWindowVideoSuperResolution"))
        self.video_auto_wipe_menu_var.set(Language.get("MainWindowVideoAutoWipe"))
        self.video_cartoon_comic_menu_var.set(Language.get("MainWindowVideoCartoonComic"))
        self.video_convert_3d_menu_var.set(Language.get("MainWindowVideoConvert3d"))
        self.video_color_restoration_menu_var.set(Language.get("MainWindowVideoColorRestoration"))
        self.video_frame_interpolation_menu_var.set(Language.get("MainWindowVideoFrameInterpolation"))
        self.video_matting_menu_var.set(Language.get("MainWindowVideoMatting"))
        self.video_organization_menu_var.set(Language.get("MainWindowVideoOrganization"))

        self.audio_label_var.set(Language.get("MainWindowAudio"))
        self.audio_vocal_split_menu_var.set(Language.get("MainWindowAudioVocalSplit"))
        self.audio_denoise_menu_var.set(Language.get("MainWindowAudioDenoise"))
        self.audio_tts_menu_var.set(Language.get("MainWindowAudioTTS"))
        self.audio_stt_menu_var.set(Language.get("MainWindowAudioSTT"))

        self.setting_menu_var.set(Language.get("MainWindowSetting"))

    def set_page(self, name):
        if name == "home":
            self.home_menu.configure(fg_color=("gray75", "gray25"))
            self.home_page.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_menu.configure(fg_color="transparent")
            self.home_page.grid_forget()
        if name == "setting":
            self.setting_menu.configure(fg_color=("gray75", "gray25"))
            self.setting_page.grid(row=0, column=1, sticky="nsew")
        else:
            self.setting_menu.configure(fg_color="transparent")
            self.setting_page.grid_forget()
        if name == "gen_chat":
            self.gen_chat_menu.configure(fg_color=("gray75", "gray25"))
            self.gen_chat_page.grid(row=0, column=1, sticky="nsew")
            self.gen_chat_page.set_show()
        else:
            self.gen_chat_menu.configure(fg_color="transparent")
            self.gen_chat_page.grid_forget()
            self.gen_chat_page.set_hide()
        if name == "image_super_resolution":
            self.image_super_resolution_menu.configure(fg_color=("gray75", "gray25"))
            self.image_super_resolution_page.grid(row=0, column=1, sticky="nsew")
            self.image_super_resolution_page.set_show()
        else:
            self.image_super_resolution_menu.configure(fg_color="transparent")
            self.image_super_resolution_page.grid_forget()
            self.image_super_resolution_page.set_hide()
        if name == "image_auto_wipe":
            self.image_auto_wipe_menu.configure(fg_color=("gray75", "gray25"))
            self.image_auto_wipe_page.grid(row=0, column=1, sticky="nsew")
            self.image_auto_wipe_page.set_show()
        else:
            self.image_auto_wipe_menu.configure(fg_color="transparent")
            self.image_auto_wipe_page.grid_forget()
            self.image_auto_wipe_page.set_hide()
        if name == "image_cartoon_comic":
            self.image_cartoon_comic_menu.configure(fg_color=("gray75", "gray25"))
            self.image_cartoon_comic_page.grid(row=0, column=1, sticky="nsew")
            self.image_cartoon_comic_page.set_show()
        else:
            self.image_cartoon_comic_menu.configure(fg_color="transparent")
            self.image_cartoon_comic_page.grid_forget()
            self.image_cartoon_comic_page.set_hide()
        if name == "image_convert_3d":
            self.image_convert_3d_menu.configure(fg_color=("gray75", "gray25"))
            self.image_convert_3d_page.grid(row=0, column=1, sticky="nsew")
            self.image_convert_3d_page.set_show()
        else:
            self.image_convert_3d_menu.configure(fg_color="transparent")
            self.image_convert_3d_page.grid_forget()
            self.image_convert_3d_page.set_hide()
        if name == "image_color_restoration":
            self.image_color_restoration_menu.configure(fg_color=("gray75", "gray25"))
            self.image_color_restoration_page.grid(row=0, column=1, sticky="nsew")
            self.image_color_restoration_page.set_show()
        else:
            self.image_color_restoration_menu.configure(fg_color="transparent")
            self.image_color_restoration_page.grid_forget()
            self.image_color_restoration_page.set_hide()
        if name == "image_frame_interpolation":
            self.image_frame_interpolation_menu.configure(fg_color=("gray75", "gray25"))
            self.image_frame_interpolation_page.grid(row=0, column=1, sticky="nsew")
            self.image_frame_interpolation_page.set_show()
        else:
            self.image_frame_interpolation_menu.configure(fg_color="transparent")
            self.image_frame_interpolation_page.grid_forget()
            self.image_frame_interpolation_page.set_hide()
        if name == "image_matting":
            self.image_matting_menu.configure(fg_color=("gray75", "gray25"))
            self.image_matting_page.grid(row=0, column=1, sticky="nsew")
            self.image_matting_page.set_show()
        else:
            self.image_matting_menu.configure(fg_color="transparent")
            self.image_matting_page.grid_forget()
            self.image_matting_page.set_hide()
        if name == "image_face_restoration":
            self.image_face_restoration_menu.configure(fg_color=("gray75", "gray25"))
            self.image_face_restoration_page.grid(row=0, column=1, sticky="nsew")
            self.image_face_restoration_page.set_show()
        else:
            self.image_face_restoration_menu.configure(fg_color="transparent")
            self.image_face_restoration_page.grid_forget()
            self.image_face_restoration_page.set_hide()
        if name == "video_super_resolution":
            self.video_super_resolution_menu.configure(fg_color=("gray75", "gray25"))
            self.video_super_resolution_page.grid(row=0, column=1, sticky="nsew")
            self.video_super_resolution_page.set_show()
        else:
            self.video_super_resolution_menu.configure(fg_color="transparent")
            self.video_super_resolution_page.grid_forget()
            self.video_super_resolution_page.set_hide()
        if name == "video_auto_wipe":
            self.video_auto_wipe_menu.configure(fg_color=("gray75", "gray25"))
            self.video_auto_wipe_page.grid(row=0, column=1, sticky="nsew")
            self.video_auto_wipe_page.set_show()
        else:
            self.video_auto_wipe_menu.configure(fg_color="transparent")
            self.video_auto_wipe_page.grid_forget()
            self.video_auto_wipe_page.set_hide()
        if name == "video_cartoon_comic":
            self.video_cartoon_comic_menu.configure(fg_color=("gray75", "gray25"))
            self.video_cartoon_comic_page.grid(row=0, column=1, sticky="nsew")
            self.video_cartoon_comic_page.set_show()
        else:
            self.video_cartoon_comic_menu.configure(fg_color="transparent")
            self.video_cartoon_comic_page.grid_forget()
            self.video_cartoon_comic_page.set_hide()
        if name == "video_convert_3d":
            self.video_convert_3d_menu.configure(fg_color=("gray75", "gray25"))
            self.video_convert_3d_page.grid(row=0, column=1, sticky="nsew")
            self.video_convert_3d_page.set_show()
        else:
            self.video_convert_3d_menu.configure(fg_color="transparent")
            self.video_convert_3d_page.grid_forget()
            self.video_convert_3d_page.set_hide()
        if name == "video_color_restoration":
            self.video_color_restoration_menu.configure(fg_color=("gray75", "gray25"))
            self.video_color_restoration_page.grid(row=0, column=1, sticky="nsew")
            self.video_color_restoration_page.set_show()
        else:
            self.video_color_restoration_menu.configure(fg_color="transparent")
            self.video_color_restoration_page.grid_forget()
            self.video_color_restoration_page.set_hide()
        if name == "video_frame_interpolation":
            self.video_frame_interpolation_menu.configure(fg_color=("gray75", "gray25"))
            self.video_frame_interpolation_page.grid(row=0, column=1, sticky="nsew")
            self.video_frame_interpolation_page.set_show()
        else:
            self.video_frame_interpolation_menu.configure(fg_color="transparent")
            self.video_frame_interpolation_page.grid_forget()
            self.video_frame_interpolation_page.set_hide()
        if name == "video_matting":
            self.video_matting_menu.configure(fg_color=("gray75", "gray25"))
            self.video_matting_page.grid(row=0, column=1, sticky="nsew")
            self.video_matting_page.set_show()
        else:
            self.video_matting_menu.configure(fg_color="transparent")
            self.video_matting_page.grid_forget()
            self.video_matting_page.set_hide()
        if name == "video_organization":
            self.video_organization_menu.configure(fg_color=("gray75", "gray25"))
            self.video_organization_page.grid(row=0, column=1, sticky="nsew")
            self.video_organization_page.set_show()
        else:
            self.video_organization_menu.configure(fg_color="transparent")
            self.video_organization_page.grid_forget()
            self.video_organization_page.set_hide()
        if name == "audio_vocal_split":
            self.audio_vocal_split_menu.configure(fg_color=("gray75", "gray25"))
            self.audio_vocal_split_page.grid(row=0, column=1, sticky="nsew")
            self.audio_vocal_split_page.set_show()
        else:
            self.audio_vocal_split_menu.configure(fg_color="transparent")
            self.audio_vocal_split_page.grid_forget()
            self.audio_vocal_split_page.set_hide()
        if name == "audio_denoise":
            self.audio_denoise_menu.configure(fg_color=("gray75", "gray25"))
            self.audio_denoise_page.grid(row=0, column=1, sticky="nsew")
            self.audio_denoise_page.set_show()
        else:
            self.audio_denoise_menu.configure(fg_color="transparent")
            self.audio_denoise_page.grid_forget()
            self.audio_denoise_page.set_hide()
        if name == "audio_tts":
            self.audio_tts_menu.configure(fg_color=("gray75", "gray25"))
            self.audio_tts_page.grid(row=0, column=1, sticky="nsew")
            self.audio_tts_page.set_show()
        else:
            self.audio_tts_menu.configure(fg_color="transparent")
            self.audio_tts_page.grid_forget()
            self.audio_tts_page.set_hide()
        if name == "audio_stt":
            self.audio_stt_menu.configure(fg_color=("gray75", "gray25"))
            self.audio_stt_page.grid(row=0, column=1, sticky="nsew")
            self.audio_stt_page.set_show()
        else:
            self.audio_stt_menu.configure(fg_color="transparent")
            self.audio_stt_page.grid_forget()
            self.audio_stt_page.set_hide()

    def set_language(self):
        self.init_language()

        self.home_page.init_language()

        self.setting_page.init_language()

        self.gen_chat_page.init_language()

        self.image_super_resolution_page.init_language()
        self.image_auto_wipe_page.init_language()
        self.image_cartoon_comic_page.init_language()
        self.image_convert_3d_page.init_language()
        self.image_color_restoration_page.init_language()
        self.image_frame_interpolation_page.init_language()
        self.image_matting_page.init_language()
        self.image_face_restoration_page.init_language()

        self.video_super_resolution_page.init_language()
        self.video_auto_wipe_page.init_language()
        self.video_cartoon_comic_page.init_language()
        self.video_convert_3d_page.init_language()
        self.video_color_restoration_page.init_language()
        self.video_frame_interpolation_page.init_language()
        self.video_matting_page.init_language()
        self.video_organization_page.init_language()

        self.audio_vocal_split_page.init_language()
        self.audio_denoise_page.init_language()
        self.audio_tts_page.init_language()
        self.audio_stt_page.init_language()

    def gen_chat_config_setting_window_show(self):
        if self.gen_chat_config_setting_window is None or not self.gen_chat_config_setting_window.winfo_exists():
            self.gen_chat_config_setting_window = GenChatConfigWindow.ConfigWindow(self)
            self.gen_chat_config_setting_window.set_show()
        else:
            self.gen_chat_config_setting_window.focus()
