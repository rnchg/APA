import customtkinter
from PIL import Image
from PIL import ImageTk

from core.consts.app_const import AppConst


class Default:
    class Images:
        app = lambda: ImageTk.PhotoImage(Image.open(f"{AppConst.assets_path}/app.png"))

        logo = customtkinter.CTkImage(Image.open(f"{AppConst.assets_path}/app.png"), size=(32, 32))

        dashboard = customtkinter.CTkImage(Image.open(f"{AppConst.assets_path}/dashboard.jpg"), size=(1600, 220))

        order = customtkinter.CTkImage(Image.open(f"{AppConst.assets_path}/order.png"), size=(800, 450))

        audio = f"{AppConst.assets_path}/audio.png"

        home = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/home.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/home.png"), size=(20, 20))

        arrow_up = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/arrow_up.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/arrow_up.png"), size=(20, 20))
        arrow_down = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/arrow_down.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/arrow_down.png"), size=(20, 20))
        arrow_left = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/arrow_left.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/arrow_left.png"), size=(20, 20))
        arrow_right = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/arrow_right.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/arrow_right.png"), size=(20, 20))

        setting = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/setting.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/setting.png"), size=(20, 20))
        theme = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/theme.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/theme.png"), size=(20, 20))
        color = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/color.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/color.png"), size=(20, 20))
        mode = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/mode.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/mode.png"), size=(20, 20))
        language = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/language.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/language.png"), size=(20, 20))
        license = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/license.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/license.png"), size=(20, 20))

        play = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/play.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/play.png"), size=(20, 20))
        stop = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/stop.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/stop.png"), size=(20, 20))
        pause = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/pause.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/pause.png"), size=(20, 20))
        forward_5 = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/forward_5.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/forward_5.png"), size=(20, 20))
        replay_5 = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/replay_5.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/replay_5.png"), size=(20, 20))

        gen_chat = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/gen_chat.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/gen_chat.png"), size=(20, 20))

        image_super_resolution = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/image_super_resolution.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/image_super_resolution.png"), size=(20, 20))
        image_auto_wipe = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/image_auto_wipe.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/image_auto_wipe.png"), size=(20, 20))
        image_cartoon_comic = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/image_cartoon_comic.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/image_cartoon_comic.png"), size=(20, 20))
        image_convert_3d = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/image_convert_3d.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/image_convert_3d.png"), size=(20, 20))
        image_color_restoration = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/image_color_restoration.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/image_color_restoration.png"), size=(20, 20))
        image_frame_interpolation = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/image_frame_interpolation.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/image_frame_interpolation.png"), size=(20, 20))
        image_matting = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/image_matting.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/image_matting.png"), size=(20, 20))
        image_face_restoration = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/image_face_restoration.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/image_face_restoration.png"), size=(20, 20))

        video_super_resolution = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/video_super_resolution.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/video_super_resolution.png"), size=(20, 20))
        video_auto_wipe = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/video_auto_wipe.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/video_auto_wipe.png"), size=(20, 20))
        video_cartoon_comic = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/video_cartoon_comic.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/video_cartoon_comic.png"), size=(20, 20))
        video_convert_3d = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/video_convert_3d.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/video_convert_3d.png"), size=(20, 20))
        video_color_restoration = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/video_color_restoration.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/video_color_restoration.png"), size=(20, 20))
        video_frame_interpolation = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/video_frame_interpolation.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/video_frame_interpolation.png"), size=(20, 20))
        video_matting = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/video_matting.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/video_matting.png"), size=(20, 20))
        video_organization = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/video_organization.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/video_organization.png"), size=(20, 20))

        audio_vocal_split = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/audio_vocal_split.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/audio_vocal_split.png"), size=(20, 20))
        audio_tts = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/audio_tts.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/audio_tts.png"), size=(20, 20))
        audio_stt = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/audio_stt.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/audio_stt.png"), size=(20, 20))
        audio_denoise = customtkinter.CTkImage(light_image=Image.open(f"{AppConst.assets_path}/dark/audio_denoise.png"), dark_image=Image.open(f"{AppConst.assets_path}/light/audio_denoise.png"), size=(20, 20))
