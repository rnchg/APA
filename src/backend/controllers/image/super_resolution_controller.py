import os
from datetime import datetime

import webview
from flask import request, Response, send_file

from core.consts.app_const import AppConst
from core.utility.current import Current
from core.helpers.file_helper import FileHelper

from core.exceptions.activation_exception import ActivationException

from controllers.base.base_controller import BaseController

from core.services.image.super_resolution_service import SuperResolutionService


class SuperResolutionController(BaseController):
    def __init__(self):
        super().__init__()

        self.input_exts = AppConst.image_exts
        self.output_exts = AppConst.image_exts
        self.base_service = SuperResolutionService()
        self.base_url = f"{self.base_api}/image/superResolution"

    def setup_routes(self):

        @self.base_server.route(f"{self.base_url}/getConfig", methods=["POST"])
        def image_super_resolution_getConfig():
            data = Current.config.image_super_resolution.to_dict()
            return self.ok(data)

        @self.base_server.route(f"{self.base_url}/setConfig", methods=["POST"])
        def image_super_resolution_setConfig():
            data = request.json["data"]
            Current.config.image_super_resolution.dict_to(data)
            return self.ok()

        @self.base_server.route(f"{self.base_url}/getFolder", methods=["POST"])
        def image_super_resolution_getFolder():
            path = request.json["path"]
            folders = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG, directory=path)
            if not folders:
                return self.badRequest(message=f"Image.SuperResolution.FolderError: path: {path}")
            return self.ok({"folder": folders[0]})

        @self.base_server.route(f"{self.base_url}/getFileGrid", methods=["POST"])
        def image_super_resolution_getFileGrid():
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
        def image_super_resolution_getFileUrl():
            file = request.json["file"]
            return self.ok({"url": f"{request.url.replace("getFileUrl", "getFileView")}?file={file}"})

        @self.base_server.route(f"{self.base_url}/getFileView", methods=["GET"])
        def image_super_resolution_getFileView():
            file = request.args["file"]
            return send_file(file)

        @self.base_server.route(f"{self.base_url}/start", methods=["POST"])
        def image_super_resolution_start():
            data = request.json["data"]
            return Response(self.start(data), content_type="text/event-stream")

        @self.base_server.route(f"{self.base_url}/stop", methods=["POST"])
        def image_super_resolution_stop():
            self.base_service.is_stop = True
            return self.ok()

        @self.base_server.route(f"{self.base_url}/open", methods=["POST"])
        def image_super_resolution_open():
            path = request.json["path"]
            if not os.path.exists(path):
                return self.badRequest(message=f"Image.SuperResolution.OpenError: path: {path}")
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
                raise Exception("Image.SuperResolution.InputError")
            output = data["output"]
            if not os.path.isdir(output):
                raise Exception("Image.SuperResolution.OutputError")
            input_files = data["input_files"]
            if not input_files:
                raise Exception("Image.SuperResolution.FileError")
            provider = data["provider"]
            if provider is None:
                raise Exception(f"Image.SuperResolution.ParamError: provider: {provider}")
            mode = data["mode"]
            if mode is None:
                raise Exception(f"Image.SuperResolution.ParamError: mode: {mode}")
            scale = data["scale"]
            if scale is None:
                raise Exception(f"Image.SuperResolution.ParamError: scale: {scale}")
            yield from self.base_service.start(input, output, input_files, provider, mode, scale)
            self.base_service.is_stop = True
            self.base_service.message = {"type": "success", "text": "Image.SuperResolution.ProcessEnd"}
        except ActivationException:
            self.base_service.is_auth = False
            self.base_service.message = {"type": "error", "text": "Image.SuperResolution.ProcessAuthError"}
        except Exception as e:
            self.base_service.is_stop = True
            self.base_service.message = {"type": "error", "text": f"{e}"}
        finally:
            self.base_service.progress = 0
            yield self.base_service.get_start_result()
