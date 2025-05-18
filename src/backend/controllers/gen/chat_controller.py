from flask import request, Response
from server import server

from core.consts.app_const import AppConst
from core.utility.current import Current

from core.exceptions.activation_exception import ActivationException

from controllers.base.base_controller import BaseController

from core.services.pages.gen.chat_service import ChatService


class ChatController(BaseController):
    def __init__(self):
        super().__init__()

        self.input_exts = AppConst.image_exts
        self.output_exts = AppConst.image_exts
        self.base_service = ChatService()
        self.base_url = f"{self.base_api}/gen/chat"

    def setup_routes(self):

        @server.route(f"{self.base_url}/getConfig", methods=["POST"])
        def audio_chat_getConfig():
            data = Current.config.gen_chat.to_dict()
            return self.ok(data)

        @server.route(f"{self.base_url}/setConfig", methods=["POST"])
        def audio_chat_setConfig():
            data = request.json["data"]
            Current.config.gen_chat.dict_to(data)
            return self.ok()

        @server.route(f"{self.base_url}/getInit", methods=["POST"])
        def gen_chat_getInit():
            return self.ok({"is_init": self.base_service.is_init})

        @server.route(f"{self.base_url}/init", methods=["POST"])
        def gen_chat_init():
            return Response(self.init(), content_type="text/event-stream")

        @server.route(f"{self.base_url}/start", methods=["POST"])
        def gen_chat_start():
            data = request.json["data"]
            return Response(self.start(data), content_type="text/event-stream")

        @server.route(f"{self.base_url}/stop", methods=["POST"])
        def gen_chat_stop():
            self.base_service.is_stop = True
            return self.ok()

    def init(self):
        try:
            self.base_service.is_auth = True
            self.base_service.progress = 0
            self.base_service.message = ""
            if self.base_service.is_init is False:
                yield from self.base_service.init()
            self.base_service.is_init = True
        except ActivationException:
            self.base_service.is_auth = False
            self.base_service.message = {"type": "error", "text": "Gen.Chat.ProcessAuthError"}
        except Exception as e:
            self.base_service.message = {"type": "error", "text": f"{e}"}
        finally:
            self.base_service.progress = 0
            yield self.base_service.get_init_result()

    def start(self, data):
        try:
            self.base_service.is_auth = True
            self.base_service.is_stop = False
            self.base_service.progress = 0
            self.base_service.message = ""
            self.base_service.token = ""
            prompt = data["prompt"]
            if not prompt:
                raise Exception("Gen.Chat.InputPromptEmpty")
            yield from self.base_service.start(prompt)
            self.base_service.is_stop = True
        except ActivationException:
            self.base_service.is_auth = False
            self.base_service.message = {"type": "error", "text": "Gen.Chat.ProcessAuthError"}
        except Exception as e:
            self.base_service.is_stop = True
            self.base_service.message = {"type": "error", "text": f"{e}"}
        finally:
            self.base_service.progress = 0
            yield self.base_service.get_start_result()
