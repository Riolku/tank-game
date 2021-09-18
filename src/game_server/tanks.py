from enum import Enum

class TankState(Enum):
    READY = 0
    BUSY = 1
    INVIS = 2

class Tank:
    def __init__(self, id, x, y, team):
        self.id = id
        self.team = team

        self.x = x
        self.y = y

        self.health = 100
        self.shielded = False
        self.state = TankState.READY
        self.speed = 10

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