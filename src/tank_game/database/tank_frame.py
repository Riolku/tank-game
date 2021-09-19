from .match_tanks import MatchTanks
from .match_frame import MatchFrame
from .aliases import *

class TankFrame(dbmodel):
    mfid = dbcol(dbint, dbforkey(MatchFrame.id), primary_key = True)
    mtid = dbcol(dbint, dbforkey(MatchTanks.id), primary_key = True)
    pos_x = dbcol(dbfloat, nullable = False)
    pos_y = dbcol(dbfloat, nullable = False)
    health = dbcol(dbfloat, nullable = False)
    state = dbcol(dbint, nullable = False)
    invis = dbcol(dbbool, nullable = False)
    ability_cd = dbcol(dbint, nullable = False)
    speed = dbcol(dbfloat, nullable = False)
    speedy = dbcol(dbbool, nullable=False)
    empowered = dbcol(dbbool, nullable=False)
    shielded = dbcol(dbbool, nullable = False)

    tank = dbrelate(MatchTanks, backref = dbbackref('frames', lazy = True))
    frame = dbrelate(MatchFrame, backref = dbbackref('tank_frames', lazy = True))
