from enum import Enum
import tanks
import json

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
    
    def get_state(self):
        out = {}

        out_tanks = []
        for tank in self.red_tanks:
            out_tanks.append(str(tank))
        for tank in self.blue_tanks:
            out_tanks.append(str(tank))
        out["tanks"] = out_tanks

        return json.dumps(out)

    def start_game(self, red_ai_id, blue_ai_id):
        #get team ai's
        #get team comps
        red_comp = []

        for t in range(len(red_comp)):
            self.red_tanks.append(tanks.Tanks[t](t, 0, 0, Team.RED))

        #get team ai's
        #get team comps
        blue_comp = []

        for t in range(len(blue_comp)):
            self.blue_tanks.append(tanks.Tanks[t](t, 0, 0 , Team.BLUE))

    def doframe(self, updates):
        ability = []
        fire = []
        move = []

        statuses_to_apply = []
        """
        (Team, id, (STATUS, EFFECT))
        """

        for update in updates:
            if(update["action"] == "ABILITY"):
                ability.append(update)
            elif(update["action"] == "FIRE"):
                fire.append(update)
            elif(update["action"] == "MOVE"):
                move.append(update)

        for update in ability:
            team = []
            tank = None

            if(update["team"]=="RED"):
                team = self.red_tanks
            elif(update["team"]=="BLUE"):
                team = self.blue_tanks
                
            tank = team[update['id']]
            if tank.state != tanks.TankState.BUSY:
                pass #do abilities (statuses)
            else:
                tank.stateticker -= 1
        
        #apply statusie
        for status in statuses_to_apply:
            team = []
            tank = None

            if(status[0]=="RED"):
                team = self.red_tanks
            elif(status[0]=="BLUE"):
                team = self.blue_tanks
                
            tank = team[status[1]]
            effect = status[2]

            if tank.state != tanks.TankState.BUSY:
                

        for update in fire:
            team = []
            tank = None

            if(update["team"]=="RED"):
                team = self.red_tanks
            elif(update["team"]=="BLUE"):
                team = self.blue_tanks
                
            tank = team[update['id']]
            if tank.state != tanks.TankState.BUSY:
                #handle obstacle/collision
                pass

        for update in move:
            team = []
            tank = None

            if(update["team"]=="RED"):
                team = self.red_tanks
            elif(update["team"]=="BLUE"):
                team = self.blue_tanks
                
            tank = team[update['id']]
            if tank.state != tanks.TankState.BUSY:
                tank.x = update["data"]["x"]
                tank.y = update["data"]["y"]
        
        return self.get_state()

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

    