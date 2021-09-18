from enum import Enum
import tanks

class Team(Enum):
    BLUE = 0
    RED = 1

class Game:
    def __init__(self):
        self.red_tanks = []
        self.blue_tanks = []

        self.terrain = []
        """[
            [["x1", "y1"], ["x2", "y2"], ["x3", "y3"], ["x4", "y4"]]
        ],"""
    
    def update(self, updates):
        for update in updates:
            team = []
            tank = None

            if(update["team"]=="RED"):
                team = self.red_tanks
            elif(update["team"]=="BLUE"):
                team = self.blue_tanks
                
            tank = team[update['id']]
            if update["action"] == "MOVE":
                tank.x = update["data"]["x"]
                tank.y = update["data"]["y"]
            elif update["action"] == "ABILITY":
                pass

"""
{
    "id":0,1,2,3,4
    "team":
    "action":"MOVE/ABILITY/FIRE"
    "MOVE_data":{
        "pos":{
            x,y
        }
    }
    "ABILITY_data":{
        pos/id
    }
    "FIRE_data":{
        id
    }
}
"""

def RunGame(red_ai_id, blue_ai_id):
    game = Game()

    #get team ai's
    #get team comps
    red_comp = []

    for t in range(len(red_comp)):
        game.red_tanks.append(tanks.Tanks[t](t, 0, 0, Team.RED))

    #get team ai's
    #get team comps
    blue_comp = []

    for t in range(len(blue_comp)):
        game.blue_tanks.append(tanks.Tanks[t](t, 0, 0 , Team.BLUE))

    