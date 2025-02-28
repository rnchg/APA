import customtkinter

from core.utility.language import Language
from domain.widgets.card.card import Card

from resources.default import Default

from views.windows.app.main_window import *


class DashboardPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.main: MainWindow = master

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_widgets()

        self.init_language()

    def init_widgets(self):
        self.content_frame = customtkinter.CTkScrollableFrame(self)
        self.content_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.logo_frame = customtkinter.CTkFrame(self.content_frame)
        self.logo_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.logo_frame.grid_columnconfigure(0, weight=1)

        self.gen_frame = customtkinter.CTkFrame(self.content_frame)
        self.gen_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.gen_frame.grid_columnconfigure(0, weight=1)
        self.gen_frame.grid_columnconfigure(1, weight=1)
        self.gen_frame.grid_columnconfigure(2, weight=1)
        self.gen_frame.grid_columnconfigure(3, weight=1)

        self.image_frame = customtkinter.CTkFrame(self.content_frame)
        self.image_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(1, weight=1)
        self.image_frame.grid_columnconfigure(2, weight=1)
        self.image_frame.grid_columnconfigure(3, weight=1)

        self.video_frame = customtkinter.CTkFrame(self.content_frame)
        self.video_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.video_frame.grid_columnconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(1, weight=1)
        self.video_frame.grid_columnconfigure(2, weight=1)
        self.video_frame.grid_columnconfigure(3, weight=1)

        self.audio_frame = customtkinter.CTkFrame(self.content_frame)
        self.audio_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.audio_frame.grid_columnconfigure(0, weight=1)
        self.audio_frame.grid_columnconfigure(1, weight=1)
        self.audio_frame.grid_columnconfigure(2, weight=1)
        self.audio_frame.grid_columnconfigure(3, weight=1)

        self.about_frame = customtkinter.CTkFrame(self.content_frame)
        self.about_frame.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

        customtkinter.CTkLabel(self.logo_frame, text="", image=Default.Images.dashboard).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.gen_chat_card_var = customtkinter.StringVar()
        self.gen_chat_card = Card(self.gen_frame, textvariable=self.gen_chat_card_var, image=Default.Images.gen_chat, command=lambda: self.main.set_page("gen_chat"))
        self.gen_chat_card.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        Card(self.gen_frame, text=" ").grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        Card(self.gen_frame, text=" ").grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        Card(self.gen_frame, text=" ").grid(row=0, column=3, padx=0, pady=0, sticky="nsew")

        self.image_super_resolution_card_var = customtkinter.StringVar()
        self.image_super_resolution_card = Card(self.image_frame, textvariable=self.image_super_resolution_card_var, image=Default.Images.image_super_resolution, command=lambda: self.main.set_page("image_super_resolution"))
        self.image_super_resolution_card.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.image_auto_wipe_card_var = customtkinter.StringVar()
        self.image_auto_wipe_card = Card(self.image_frame, textvariable=self.image_auto_wipe_card_var, image=Default.Images.image_auto_wipe, command=lambda: self.main.set_page("image_auto_wipe"))
        self.image_auto_wipe_card.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        self.image_cartoon_comic_card_var = customtkinter.StringVar()
        self.image_cartoon_comic_card = Card(self.image_frame, textvariable=self.image_cartoon_comic_card_var, image=Default.Images.image_cartoon_comic, command=lambda: self.main.set_page("image_cartoon_comic"))
        self.image_cartoon_comic_card.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

        self.image_convert_3d_card_var = customtkinter.StringVar()
        self.image_convert_3d_card = Card(self.image_frame, textvariable=self.image_convert_3d_card_var, image=Default.Images.image_convert_3d, command=lambda: self.main.set_page("image_convert_3d"))
        self.image_convert_3d_card.grid(row=0, column=3, padx=0, pady=0, sticky="nsew")

        self.image_color_restoration_card_var = customtkinter.StringVar()
        self.image_color_restoration_card = Card(self.image_frame, textvariable=self.image_color_restoration_card_var, image=Default.Images.image_color_restoration, command=lambda: self.main.set_page("image_color_restoration"))
        self.image_color_restoration_card.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        self.image_frame_interpolation_card_var = customtkinter.StringVar()
        self.image_frame_interpolation_card = Card(self.image_frame, textvariable=self.image_frame_interpolation_card_var, image=Default.Images.image_frame_interpolation, command=lambda: self.main.set_page("image_frame_interpolation"))
        self.image_frame_interpolation_card.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

        self.image_matting_card_var = customtkinter.StringVar()
        self.image_matting_card = Card(self.image_frame, textvariable=self.image_matting_card_var, image=Default.Images.image_matting, command=lambda: self.main.set_page("image_matting"))
        self.image_matting_card.grid(row=1, column=2, padx=0, pady=0, sticky="nsew")

        self.image_face_restoration_card_var = customtkinter.StringVar()
        self.image_face_restoration_card = Card(self.image_frame, textvariable=self.image_face_restoration_card_var, image=Default.Images.image_face_restoration, command=lambda: self.main.set_page("image_face_restoration"))
        self.image_face_restoration_card.grid(row=1, column=3, padx=0, pady=0, sticky="nsew")

        self.video_super_resolution_card_var = customtkinter.StringVar()
        self.video_super_resolution_card = Card(self.video_frame, textvariable=self.video_super_resolution_card_var, image=Default.Images.video_super_resolution, command=lambda: self.main.set_page("video_super_resolution"))
        self.video_super_resolution_card.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.video_auto_wipe_card_var = customtkinter.StringVar()
        self.video_auto_wipe_card = Card(self.video_frame, textvariable=self.video_auto_wipe_card_var, image=Default.Images.video_auto_wipe, command=lambda: self.main.set_page("video_auto_wipe"))
        self.video_auto_wipe_card.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        self.video_cartoon_comic_card_var = customtkinter.StringVar()
        self.video_cartoon_comic_card = Card(self.video_frame, textvariable=self.video_cartoon_comic_card_var, image=Default.Images.video_cartoon_comic, command=lambda: self.main.set_page("video_cartoon_comic"))
        self.video_cartoon_comic_card.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

        self.video_convert_3d_card_var = customtkinter.StringVar()
        self.video_convert_3d_card = Card(self.video_frame, textvariable=self.video_convert_3d_card_var, image=Default.Images.video_convert_3d, command=lambda: self.main.set_page("video_convert_3d"))
        self.video_convert_3d_card.grid(row=0, column=3, padx=0, pady=0, sticky="nsew")

        self.video_color_restoration_card_var = customtkinter.StringVar()
        self.video_color_restoration_card = Card(self.video_frame, textvariable=self.video_color_restoration_card_var, image=Default.Images.video_color_restoration, command=lambda: self.main.set_page("video_color_restoration"))
        self.video_color_restoration_card.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        self.video_frame_interpolation_card_var = customtkinter.StringVar()
        self.video_frame_interpolation_card = Card(self.video_frame, textvariable=self.video_frame_interpolation_card_var, image=Default.Images.video_frame_interpolation, command=lambda: self.main.set_page("video_frame_interpolation"))
        self.video_frame_interpolation_card.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

        self.video_matting_card_var = customtkinter.StringVar()
        self.video_matting_card = Card(self.video_frame, textvariable=self.video_matting_card_var, image=Default.Images.video_matting, command=lambda: self.main.set_page("video_matting"))
        self.video_matting_card.grid(row=1, column=2, padx=0, pady=0, sticky="nsew")

        self.video_organization_card_var = customtkinter.StringVar()
        self.video_organization_card = Card(self.video_frame, textvariable=self.video_organization_card_var, image=Default.Images.video_organization, command=lambda: self.main.set_page("video_organization"))
        self.video_organization_card.grid(row=1, column=3, padx=0, pady=0, sticky="nsew")

        self.audio_vocal_split_card_var = customtkinter.StringVar()
        self.audio_vocal_split_card = Card(self.audio_frame, textvariable=self.audio_vocal_split_card_var, image=Default.Images.audio_vocal_split, command=lambda: self.main.set_page("audio_vocal_split"))
        self.audio_vocal_split_card.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.audio_denoise_card_var = customtkinter.StringVar()
        self.audio_denoise_card = Card(self.audio_frame, textvariable=self.audio_denoise_card_var, image=Default.Images.audio_denoise, command=lambda: self.main.set_page("audio_denoise"))
        self.audio_denoise_card.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        self.audio_tts_card_var = customtkinter.StringVar()
        self.audio_tts_card = Card(self.audio_frame, textvariable=self.audio_tts_card_var, image=Default.Images.audio_tts, command=lambda: self.main.set_page("audio_tts"))
        self.audio_tts_card.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

        self.audio_stt_card_var = customtkinter.StringVar()
        self.audio_stt_card = Card(self.audio_frame, textvariable=self.audio_stt_card_var, image=Default.Images.audio_stt, command=lambda: self.main.set_page("audio_stt"))
        self.audio_stt_card.grid(row=0, column=3, padx=0, pady=0, sticky="nsew")

        self.about_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.about_frame, textvariable=self.about_label_var, font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        Card(self.about_frame, text="Email: Rnchg@Hotmail.com").grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        Card(self.about_frame, text="Github: github.com/rnchg/apa").grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
        Card(self.about_frame, text="Gitee: gitee.com/rnchg/apa").grid(row=1, column=2, padx=10, pady=0, sticky="nsew")
        Card(self.about_frame, text="Youtube: Light Cloud Wind").grid(row=2, column=0, padx=10, pady=0, sticky="nsew")
        Card(self.about_frame, text="Bilibili: 风轻云也净").grid(row=2, column=1, padx=10, pady=0, sticky="nsew")
        Card(self.about_frame, text="QQ: 6085398").grid(row=2, column=2, padx=10, pady=0, sticky="nsew")

    def init_language(self):
        self.gen_chat_card_var.set(Language.get("DashboardPageGenChat"))

        self.image_super_resolution_card_var.set(Language.get("DashboardPageImageSuperResolution"))
        self.image_auto_wipe_card_var.set(Language.get("DashboardPageImageAutoWipe"))
        self.image_cartoon_comic_card_var.set(Language.get("DashboardPageImageCartoonComic"))
        self.image_convert_3d_card_var.set(Language.get("DashboardPageImageConvert3d"))
        self.image_color_restoration_card_var.set(Language.get("DashboardPageImageColorRestoration"))
        self.image_frame_interpolation_card_var.set(Language.get("DashboardPageImageFrameInterpolation"))
        self.image_matting_card_var.set(Language.get("DashboardPageImageMatting"))
        self.image_face_restoration_card_var.set(Language.get("DashboardPageImageFaceRestoration"))

        self.video_super_resolution_card_var.set(Language.get("DashboardPageVideoSuperResolution"))
        self.video_auto_wipe_card_var.set(Language.get("DashboardPageVideoAutoWipe"))
        self.video_cartoon_comic_card_var.set(Language.get("DashboardPageVideoCartoonComic"))
        self.video_convert_3d_card_var.set(Language.get("DashboardPageVideoConvert3d"))
        self.video_color_restoration_card_var.set(Language.get("DashboardPageVideoColorRestoration"))
        self.video_frame_interpolation_card_var.set(Language.get("DashboardPageVideoFrameInterpolation"))
        self.video_matting_card_var.set(Language.get("DashboardPageVideoMatting"))
        self.video_organization_card_var.set(Language.get("DashboardPageVideoOrganization"))

        self.audio_vocal_split_card_var.set(Language.get("DashboardPageAudioVocalSplit"))
        self.audio_denoise_card_var.set(Language.get("DashboardPageAudioDenoise"))
        self.audio_tts_card_var.set(Language.get("DashboardPageAudioTTS"))
        self.audio_stt_card_var.set(Language.get("DashboardPageAudioSTT"))

        self.about_label_var.set(Language.get("ApplicationSupport"))
