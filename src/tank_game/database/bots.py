from .users import Users
from .aliases import *

class Bots(dbmodel):
    id = dbcol(dbint, primary_key = True)
    uid = dbcol(dbint, dbforkey(Users.id), nullable = False)
    code = dbcol(dbstr(65536), nullable = False)

    user = dbrelate(Users, backref = dbbackref('bots', lazy = True))
