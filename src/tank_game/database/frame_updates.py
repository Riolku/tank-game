from .match_tanks import MatchTanks
from .match_frame import MatchFrame
from .aliases import *

class FrameUpdates(dbmodel):
    id = dbcol(dbint, primary_key = True)
    mfid = dbcol(dbint, dbforkey(MatchFrame.id), nullable = False)
    mtid = dbcol(dbint, dbforkey(MatchTanks.id), nullable = False)
    action = dbcol(dbstr(16), nullable = False)
    data = dbcol(dbstr(4096), nullable = False)

    tank = dbrelate(MatchTanks, backref = dbbackref('updates', lazy = True))
    frame = dbrelate(MatchFrame, backref = dbbackref('frame_updates', lazy = True))
