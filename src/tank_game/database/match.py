from .bots import Bots
from .aliases import *

class Match(dbmodel):
    id = dbcol(dbint, primary_key = True)
    red_uid = dbcol(dbint, dbforkey(Bots.uid), nullable = False)
    blue_uid = dbcol(dbint, dbforkey(Bots.uid), nullable = False)

    red_bot = dbrelate(Bots, backref = dbbackref('matches', lazy = True))
    blue_bot = dbrelate(Bots, backref = dbbackref('matches', lazy = True))
