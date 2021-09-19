from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
app.config.from_object("tank_game.settings")
app.config.from_object("tank_game.local_settings")

CORS(app)

celery = Celery(app.import_name)

db = SQLAlchemy(app)
