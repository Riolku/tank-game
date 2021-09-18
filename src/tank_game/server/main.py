# -*- coding: utf-8 -*-

import math, os, sys, time

from flask import Flask, render_template, request
from flask_cors import CORS

from auth import *

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024


def render(*args, **kwargs):
    return render_template(*args, **kwargs, user=user)


@app.route("/")
def serve_root():
    return render("index.html"), 200


@app.route("/submit", methods=["GET"])
def serve_submit_page():
    return render("submit.html"), 200


@app.route("/submit", methods=["POST"])
def accept_submission():
    if request.form.get("switch") == "on":
        file = request.files["file"]
        path = f"/tmp/tank-game/{time.time()}"
        try:
            file.save(path)
        except:
            os.mkdir("/tmp/tank-game")
            file.save(path)
        with open(path, "r") as f:
            code = f.read()
    else:
        code = request.form["code"]
    print(code)
    return "TODO", 200


@app.route("/replay-viewer/<int:match>")
def replay_viewer(match):
    return render_template("replay-viewer.html", match=match), 200


@app.route("/match-data/<int:match>")
def match_data(match):
    # TODO get actual match data
    return [
        [
            [[10, 0], [0, 10], [200, 300], [300, 200]],
            [[10, 600], [0, 590], [200, 300], [300, 400]],
        ],
        ["hyper-neutrino", "riolku"],
        [
            ["repair", "artillery", "assassin", "shield", "shield"],
            ["kamikaze", "scout", "mortar", "hack", "shield"],
        ],
        [
            [
                [100, 100, 100, 0, -1, 0, 1],  # repair the artillery
                [100, 200, 100, 0, 0, 0, -1],  # fire directly to the east
                [100, 300, 100, 0, -1, 0, 0],  # gain MS
                [100, 400, 100, 0, -1, 0, 0],  # shield around
                [
                    100,
                    500,
                    100,
                    0,
                    math.pi / 2,
                    0,
                    -1,
                ],  # fire directly to the north
            ],
            [
                [700, 100, 100, 0, -1, 0, 0],  # explode
                [700, 200, 100, 0, -1, 0, 0],  # go invisible
                [700, 300, 100, 0, -1, 0, [500, 300]],  # throw bomb at center
                [700, 400, 100, 0, math.pi, 0, -1],  # fire directly to the west
                [
                    700,
                    500,
                    100,
                    0,
                    math.pi * 3 / 2,
                    0,
                    -1,
                ],  # fire directly to the south
            ],
            [-1, 100],
        ],
    ]


@app.errorhandler(404)
def not_found(e):
    return render("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render("500.html"), 500
