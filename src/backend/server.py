import json
import os
import webbrowser
from functools import wraps

from flask import Flask, jsonify, render_template, request

import webview

gui_dir = os.path.join(os.path.dirname(__file__), "..", "gui")

if not os.path.exists(gui_dir):
    gui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui")

server = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir, static_url_path="/")
server.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1


def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = json.loads(request.data)
        token = data.get("token")
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            raise Exception("Authentication error")

    return wrapper


@server.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response


@server.route("/")
def landing():
    return render_template("index.html", token=webview.token)


@server.route("/fullscreen", methods=["POST"])
@verify_token
def fullscreen():
    webview.windows[0].toggle_fullscreen()
    return jsonify({})


@server.route("/open-url", methods=["POST"])
@verify_token
def open_url():
    url = request.json["url"]
    webbrowser.open_new_tab(url)
    return jsonify({})
