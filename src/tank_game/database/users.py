from .aliases import *

class Users(dbmodel):
    id = dbcol(dbint, primary_key = True)
    username = dbcol(dbstr(256), unique = True, nullable = False)
    password = dbcol(dbbinary, nullable = False)
