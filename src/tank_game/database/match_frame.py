from .match import Match
from .aliases import *

class MatchFrame(dbmodel):
    id = dbcol(dbint, primary_key = True)
    mid = dbcol(dbint, dbforkey(Match.id), nullable = False)
    frame_no = dbcol(dbint, nullable = False)

    match = dbrelate(Match, backref = dbbackref('frames', lazy = True))
