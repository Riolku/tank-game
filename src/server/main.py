# -*- coding: utf-8 -*-

import sys

from flask import Flask, render_template, request
from flask_cors import CORS

from auth import *

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
CORS(app)


def render(*args, **kwargs):
    return render_template(*args, **{**kwargs, "user": user})


@app.route("/")
def serve_root():
    return render("index.html"), 200


@app.errorhandler(404)
def not_found(e):
    return render("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render("500.html"), 500


if __name__ == "__main__":
    arguments = sys.argv[1:]
    port = 5060
    debug = False
    while arguments:
        arg = arguments.pop(0)
        if arg == "-d" or arg == "--debug":
            debug = True
        elif arg == "-p" or arg == "--port":
            if arguments:
                rawport = arguments.pop(0)
                if rawport.isdigit():
                    port = int(rawport)
                else:
                    raise SystemExit(
                        "Argument after --port / -p must be a positive integer."
                    )
            else:
                raise SystemExit("There must be an argument after --port / -p")
        else:
            raise SystemExit(f"Unrecognized argument `{arg}`")
    app.run(host="0.0.0.0", port=port, debug=debug)
