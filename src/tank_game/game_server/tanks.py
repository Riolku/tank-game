from enum import Enum
import json

HEAL_AMT = 5
HEAL_STUN = 5
HEAL_CD = 10

ART_BUFF = 5
ART_CD = 5
ART_DUR = 3

MOR_DMG = 30
MOR_RAD = 50
MOR_STUN = 1
MOR_CD = 20

ASS_BUFF = 5
ASS_CD = 5
ASS_DUR = 3

SHLD_CD = 10
SHLD_DUR = 5

KAMI_DMG = 50
KAMI_RAD = 5

SCT_DUR = 2
SCT_CD = 5

HTN_DUR=5
HTN_CD=7

class TankState:
    READY = 0
    BUSY = 1
    DEAD = 2

class Status:
    HEAL=0
    DAMAGE=1
    STUN=2
    SHIELD=3
    INVIS=4
    HACK=5

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

        self.abilitycd = 0
        self.abilitydur = 0
        self.shielddur = 0

        self.attack = 2
        self.empowered = False
        self.speedy = False

    def get_json(self):
        return {
            "id":self.id,
            "team":self.team,
            "type":self.type,
            "pos_x":self.x,
            "pos_y":self.y,
            "health":self.health,
            "state":self.state,
            "invis":self.invis,
            "ability_cd":self.abilitycd,
            "speed":self.speed,
            "shielded":self.shielded,
            "empowered":self.empowered,
            "speedy":self.speedy
        }


    def update(self):
        if(self.abilitycd>0):
            self.abilitycd-=1
        if(self.stateticker>0):
            self.stateticker-=1
        elif(self.stateticker== 0 and self.state == TankState.BUSY):
            self.state = TankState.READY

        if(self.abilitydur>0):
            self.abilitydur-=1
        elif(self.abilitydur == 0):
            self.cancel_ability()
            self.abilitydur = -1

        if(self.shielddur == 1):
            self.shielded = False
            self.shielddur = 0

    def damage(self, damage):
        if not self.shielded:
            self.health -= damage
            if self.health <= 0:
                self.state=TankState.DEAD
        else:
            self.shielded = False
            self.shielddur = 0

    def heal(self, amount):
        self.health += amount
        self.health = min(self.health, 100)

    def stun(self, amount):
        self.state = TankState.BUSY
        self.stateticker = amount

    def shield(self):
        self.shielded = True
        self.shielddur = SHLD_DUR

    def ability_cooldown(self, length):
        self.abilitycd = length

    def ability_duration(self, length):
        self.abilitydur = length

    def ability(self, team_tanks, enemy_tanks, data):
        return self.abilitycd == 0

    def cancel_ability(self):
        pass

    def hack(self):
        self.abilitycd = HTN_DUR

    def invis(self):
        self.invis = True

    def is_dead(self):
        return self.state == TankState.DEAD

class RepairTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "repair"

    def ability(self, team_tanks, enemy_tanks, data): #data:id
        if(super().ability(team_tanks, enemy_tanks, data)):
            events = []

            events.append([data, self.team, Status.HEAL, HEAL_AMT])
            events.append([data, self.team, Status.STUN, HEAL_STUN])

            self.ability_cooldown(HEAL_CD)

            return events

class ArtilleryTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "artillery"

    def ability(self, team_tanks, enemy_tanks, data): #data:NONE/self id
        if(super().ability(team_tanks, enemy_tanks, data)) and not self.empowered:
            self.empowered = True
            self.attack += ART_BUFF
            self.ability_cooldown(ART_CD)
            self.ability_duration(ART_DUR)

        return []

    def cancel_ability(self):
        if self.empowered:
            self.empowered = False
            self.attack -= ART_BUFF

class AssassinTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "assassin"

    def ability(self, team_tanks, enemy_tanks, data):#data:NONE/self id
        if(super().ability(team_tanks, enemy_tanks, data)):
            self.speedy = True
            self.speed += ASS_BUFF
            self.ability_duration(ASS_DUR)
            self.ability_cooldown(ASS_CD)

        return []

    def cancel_ability(self):
        self.speedy = False
        self.speed -= ASS_BUFF


class ShieldTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "shield"

    def ability(self, team_tanks, enemy_tanks, data):#data:id
        events = []
        if(super().ability(team_tanks, enemy_tanks, data)):
            self.ability_cooldown(SHLD_CD)
            events = [[data, self.team, Status.SHIELD, 0]]
        return events

class KamikazeTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "kamikaze"

    def ability(self, team_tanks, enemy_tanks, data):#data:(x,y)
        events = []
        if(super().ability(team_tanks, enemy_tanks, data)):
            tanks = team_tanks+enemy_tanks
            for tank in tanks:
                if self.x-KAMI_RAD < tank.x < self.x+KAMI_RAD and self.y-KAMI_RAD < tank.y < self.y+KAMI_RAD:
                    events.append([tank.id, tank.team, Status.DAMAGE, KAMI_DMG])

            events.append([self.id, self.team, Status.DAMAGE, 727])
        return events

class ScoutTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "scout"

    def ability(self, team_tanks, enemy_tanks, data):#data:NONE/self id
        events = []
        if(super().ability(team_tanks, enemy_tanks, data)):
            events = [[self.id, self.team, Status.INVIS, 0]]
            self.ability_cooldown(SCT_CD)
            self.ability_duration(SCT_DUR)
        return events

class MortarTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "mortar"

    def ability(self, team_tanks, enemy_tanks, data): #data:(x,y)
        events = []
        if(super().ability(team_tanks, enemy_tanks, data)):

            x=data[0]
            y=data[1]
            tanks = team_tanks+enemy_tanks
            for tank in tanks:
                if x-MOR_RAD < tank.x < x+MOR_RAD and y-MOR_RAD < tank.y < y+MOR_RAD:
                    events.append([tank.id, tank.team, Status.DAMAGE, MOR_DMG])
                    events.append([tank.id, tank.team, Status.STUN, MOR_STUN])

            self.ability_cooldown(MOR_CD)
        return events

class HTNTank(Tank):
    def __init__(self, id, x, y, team):
        super().__init__(id, x, y, team)
        self.type = "htn"

    def ability(self, team_tanks, enemy_tanks, data):#data:id
        events = []
        if(super().ability(team_tanks, enemy_tanks, data)):
            events = [[data, enemy_tanks, Status.HACK, 0]]
            self.ability_cooldown(HTN_CD)
        return events

Tanks = {
    "hack":HTNTank,
    "mortar":MortarTank,
    "scout":ScoutTank,
    "kamikaze":KamikazeTank,
    "shield":ShieldTank,
    "assassin":AssassinTank,
    "artillery":ArtilleryTank,
    "repair": RepairTank
}
