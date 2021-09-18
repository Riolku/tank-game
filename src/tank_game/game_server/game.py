from enum import Enum

class TankState(Enum):
    READY = 0
    BUSY = 1

class Team(Enum):
    BLUE = 0
    RED = 1

class Tank:
    def __init__(self, id, x, y, team):
        self.id = id
        self.team = team

        self.x = x
        self.y = y

        self.health = 0
        self.shielded = False
        self.state = TankState.READY

class Game:
    def __init__(self):
        red_tanks = []
        blue_tanks = []

        terrain = []
        """[
            [["x1", "y1"], ["x2", "y2"], ["x3", "y3"], ["x4", "y4"]]
        ],"""

def RunGame(red_ai_id, blue_ai_id):
    game = Game()

    #get team ai's
    #get team comps
    red_comp = []