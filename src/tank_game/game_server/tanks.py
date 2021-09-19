from enum import Enum
import json

class TankState(Enum):
    READY = 0
    BUSY = 1
    DEAD = 2

class Tank:
    def __init__(self, id, x, y, team):
        self.id = id
        self.team = team

        self.x = x
        self.y = y

        self.health = 100
        self.shielded = False
        self.state = TankState.READY
        self.stateticker = 0
        self.speed = 10
        self.type = ""
        self.invis = False
        self.abilitycooldown = 0
    
    def __str__(self):
        return json.dumps({
            "id":self.id,
            "team":self.team,
            "type":self.type,
            "pos_x":self.x,
            "pos_y":self.y,
            "health":self.health,
            "state":self.state,
            "invis":self.invis
        })

class RepairTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "Repair"

class ArtilleryTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "Artillery"

class AssassinTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "Assassin"

class ShieldTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "Shield"

class KamikazeTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "Kamikaze"

class ScoutTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "Scout"

class MortarTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "Mortar"

class HTNTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "HTN"

Tanks = {
    "HTN":HTNTank,
    "Mortar":MortarTank,
    "Scout":ScoutTank,
    "Kamikaze":KamikazeTank,
    "Shield":ShieldTank,
    "Assassin":AssassinTank,
    "Artillery":ArtilleryTank,
    "Repair": RepairTank
}