from tank_game import db

from .users import Users
from .bots import Bots
from .match import Match

db.create_all()
