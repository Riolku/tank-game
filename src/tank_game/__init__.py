from flask import Flask
from flask_cors import CORS

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
