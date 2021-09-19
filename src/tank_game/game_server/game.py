from enum import Enum
from tank_game.game_server import tanks
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

        return out

    def start_game(self, red_comp, blue_comp):
        for t in range(len(red_comp)):
            self.red_tanks.append(tanks.Tanks[red_comp[t]](t, 0, 0, Team.RED))

        for t in range(len(blue_comp)):
            self.blue_tanks.append(tanks.Tanks[blue_comp[t]](t, 0, 0 , Team.BLUE))

    def doframe(self, updates):
        ability = []
        fire = []
        move = []

        event_q = []
        """
        (Team, id, (STATUS, EFFECT))
        statuses: heal, stun, damage
        """

        """
        update:{
            "id":0,1,2,3,4
            "team":red/blue
            "action":"MOVE/ABILITY/FIRE"
            "data":{}
        }
        """

        for update in updates:
            if(update["action"] == "ABILITY"):
                ability.append(update)
            elif(update["action"] == "FIRE"):
                fire.append(update)
            elif(update["action"] == "MOVE"):
                move.append(update)

        for tank in self.red_tanks+self.blue_tanks:
            tank.update()

        #Handle ability usage
        for update in ability:
            team = []
            enemy = []
            tank = None

            if(update["team"]=="RED"):
                team = self.red_tanks
                enemy = self.blue_tanks
            elif(update["team"]=="BLUE"):
                team = self.blue_tanks
                enemy = self.red_tanks

            tank = team[update['id']]
            if tank.state != tanks.TankState.BUSY:
                for event in tank.ability(team, enemy, update["data"]):
                    event_q.append(event)

        #apply statuses
        for status in event_q:
            team = []
            tank = None

            if(status[0]=="RED"):
                team = self.red_tanks
            elif(status[0]=="BLUE"):
                team = self.blue_tanks

            tank = team[status[1]]

            eff_type = status[2]
            eff_amt = status[3]

            if tank.state != tanks.TankState.BUSY:
                if eff_type == tanks.Status.HEAL:
                    tank.heal(eff_amt)
                elif eff_type == tanks.Status.DAMAGE:
                    tank.damage(eff_amt)
                elif eff_type == tanks.Status.STUN:
                    tank.stun(eff_amt)
                elif eff_type == tanks.Status.SHIELD:
                    tank.shield()
                elif eff_type ==tanks.Status.HACK:
                    tank.hack()

        event_q2 = []

        #fire lazers
        for update in fire:
            team = []
            tank = None

            if(update["team"]=="RED"):
                team = self.red_tanks
                enemy = self.blue_tanks
            elif(update["team"]=="BLUE"):
                team = self.blue_tanks
                enemy = self.red_tanks

            tank = team[update['id']]
            if tank.state not in (tanks.TankState.BUSY, tanks.TankState.DEAD):
                #handle obstacle/collision (IF YOU ARE LITERALLY INSANE)
                event_q2.append([update["data"], enemy, tanks.Status.DAMAGE, tank.attack])

        for status in event_q:
            team = []
            tank = None

            if(status[1]=="RED"):
                team = self.red_tanks
            elif(status[1]=="BLUE"):
                team = self.blue_tanks

            tank = team[status[0]]

            eff_type = status[2]
            eff_amt = status[3]

            if tank.state != tanks.TankState.BUSY:
                if eff_type == tanks.Status.DAMAGE:
                    tank.damage(eff_amt)

        #update positions
        for update in move:
            team = []
            tank = None

            if(update["team"]=="RED"):
                team = self.red_tanks
            elif(update["team"]=="BLUE"):
                team = self.blue_tanks

            tank = team[update['id']]
            if tank.state != tanks.TankState.BUSY:
                tank.x = update["data"][0]
                tank.y = update["data"][1]

        frame_info = self.get_state()
        frame_info["updates"] = updates

        return json.dumps(frame_info)

"""
{
    "id":0,1,2,3,4
    "team":
    "action":"MOVE/ABILITY/FIRE"
    "MOVE_data":(x, y)
    "ABILITY_data":(x,y)/(id)
    "FIRE_data":id
}
"""
