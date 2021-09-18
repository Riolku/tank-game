from tank_game import db
from .aliases import *

class Users(dbmodel):
    id = dbcol(dbint, primary_key = True)
    username = dbcol(dbstr(256), unique = True, nullable = False)
