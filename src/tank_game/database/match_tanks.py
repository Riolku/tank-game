from .match import Match
from .aliases import *

class MatchTanks(dbmodel):
    id = dbcol(dbint, primary_key = True)
    mid = dbcol(dbint, dbforkey(Match.id), nullable = False)
    type = dbcol(dbstr(64), nullable = False)
    colour = dbcol(dbstr(32), nullable = False)
    number = dbcol(dbint, nullable = False)

    match = dbrelate(Match)
