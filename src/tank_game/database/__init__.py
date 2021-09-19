from tank_game import db

from .users import Users
from .match import Match
from .match_frame import MatchFrame
from .match_tanks import MatchTanks
from .tank_frame import TankFrame

db.create_all()
