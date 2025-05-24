import os
from datetime import datetime

import webview
from flask import request, Response, send_file

from core.consts.app_const import AppConst
from core.utility.current import Current
from core.helpers.file_helper import FileHelper

from core.exceptions.activation_exception import ActivationException

from controllers.base.base_controller import BaseController

from core.services.audio.denoise_service import DenoiseService


class DenoiseController(BaseController):
    def __init__(self):
        super().__init__()

        self.input_exts = AppConst.audio_exts
        self.output_exts = AppConst.audio_exts
        self.base_service = DenoiseService()
        self.base_url = f"{self.base_api}/audio/denoise"

    def setup_routes(self):
        
        @self.base_server.route(f"{self.base_url}/getConfig", methods=["POST"])
        def audio_denoise_getConfig():
            data = Current.config.audio_denoise.to_dict()
            return self.ok(data)

        @self.base_server.route(f"{self.base_url}/setConfig", methods=["POST"])
        def audio_denoise_setConfig():
            data = request.json["data"]
            Current.config.audio_denoise.dict_to(data)
            return self.ok()

        @self.base_server.route(f"{self.base_url}/getFolder", methods=["POST"])
        def audio_denoise_getFolder():
            path = request.json["path"]
            folders = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG, directory=path)
            if not folders:
                return self.badRequest(message=f"Audio.Denoise.FolderError: path: {path}")
            return self.ok({"folder": folders[0]})

        @self.base_server.route(f"{self.base_url}/getFileGrid", methods=["POST"])
        def audio_denoise_getFileGrid():
            folder = request.json["folder"]
            exts = request.json["exts"]
            if exts == "input":
                paths = FileHelper.get_paths(folder, self.input_exts)
            elif exts == "output":
                paths = FileHelper.get_paths(folder, self.output_exts)
            else:
                paths = []
            files = [{"path": path, "basename": os.path.basename(path), "size": os.path.getsize(path), "mtime": datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")} for path in paths]
            return self.ok({"files": files})

        @self.base_server.route(f"{self.base_url}/getFileUrl", methods=["POST"])
        def audio_denoise_getFileUrl():
            file = request.json["file"]
            return self.ok({"url": f"{request.url.replace("getFileUrl", "getFileView")}?file={file}"})

        @self.base_server.route(f"{self.base_url}/getFileView", methods=["GET"])
        def audio_denoise_getFileView():
            file = request.args["file"]
            return send_file(file)

        @self.base_server.route(f"{self.base_url}/start", methods=["POST"])
        def audio_denoise_start():
            data = request.json["data"]
            return Response(self.start(data), content_type="text/event-stream")

        @self.base_server.route(f"{self.base_url}/stop", methods=["POST"])
        def audio_denoise_stop():
            self.base_service.is_stop = True
            return self.ok()

        @self.base_server.route(f"{self.base_url}/open", methods=["POST"])
        def audio_denoise_open():
            path = request.json["path"]
            if not os.path.exists(path):
                return self.badRequest(message=f"Audio.Denoise.OpenError: path: {path}")
            os.startfile(path)
            return self.ok()

    def start(self, data):
        try:
            self.base_service.is_auth = True
            self.base_service.is_stop = False
            self.base_service.progress = 0
            self.base_service.message = ""
            input = data["input"]
            if not os.path.isdir(input):
                raise Exception("Audio.Denoise.InputError")
            output = data["output"]
            if not os.path.isdir(output):
                raise Exception("Audio.Denoise.OutputError")
            input_files = data["input_files"]
            if not input_files:
                raise Exception("Audio.Denoise.FileError")
            provider = data["provider"]
            if provider is None:
                raise Exception(f"Audio.Denoise.ParamError: provider: {provider}")
            mode = data["mode"]
            if mode is None:
                raise Exception(f"Audio.Denoise.ParamError: mode: {mode}")
            yield from self.base_service.start(input, output, input_files, provider, mode)
            self.base_service.is_stop = True
            self.base_service.message = {"type": "success", "text": "Audio.Denoise.ProcessEnd"}
        except ActivationException:
            self.base_service.is_auth = False
            self.base_service.message = {"type": "error", "text": "Audio.Denoise.ProcessAuthError"}
        except Exception as e:
            self.base_service.is_stop = True
            self.base_service.message = {"type": "error", "text": f"{e}"}
        finally:
            self.base_service.progress = 0
            yield self.base_service.get_start_result()
