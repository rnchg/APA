from services.web_service import WebService, jsonify


class BaseController:
    def __init__(self):
        # self.base_api = "/api/v1"
        self.base_api = "/prod-api/api/v1"
        self.base_server = WebService.server

    def ok(self, data={}):
        result = {"success": True, "code": 200, "data": data}
        return jsonify(result)

    def badRequest(self, message=""):
        result = {"success": False, "code": 400, "message": message}
        return jsonify(result)
