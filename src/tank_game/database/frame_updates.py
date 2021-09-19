from .match_tanks import MatchTanks
from .match_frame import MatchFrame
from .aliases import *

class FrameUpdates(dbmodel):
    mfid = dbcol(dbint, dbforkey(MatchFrame.id), primary_key = True)
    mtid = dbcol(dbint, dbforkey(MatchTanks.id), primary_key = True)
    action = dbcol(dbstr(16), nullable = False)
    data = dbcol(dbstr(4096), nullable = False)

    tank = dbrelate(MatchTanks, backref = dbbackref('updates', lazy = True))
    frame = dbrelate(MatchFrame, backref = dbbackref('frame_updates', lazy = True))
