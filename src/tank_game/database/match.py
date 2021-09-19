from .users import Users
from .aliases import *

class Match(dbmodel):
    id = dbcol(dbint, primary_key = True)
    red_uid = dbcol(dbint, dbforkey(Users.id), nullable = False)
    blue_uid = dbcol(dbint, dbforkey(Users.id), nullable = False)

    red_user = dbrelate(Users, backref = dbbackref('matches', lazy = True))
    blue_user = dbrelate(Users, backref = dbbackref('matches', lazy = True))
