from .users import Users
from .aliases import *

class Match(dbmodel):
    id = dbcol(dbint, primary_key = True)
    red_uid = dbcol(dbint, dbforkey(Users.id), nullable = False)
    blue_uid = dbcol(dbint, dbforkey(Users.id), nullable = False)

    red_user = dbrelate(Users, foreign_keys = [ red_uid ], backref = dbbackref('red_matches', lazy = True))
    blue_user = dbrelate(Users, foreign_keys = [ blue_uid ], backref = dbbackref('blue_matches', lazy = True))
