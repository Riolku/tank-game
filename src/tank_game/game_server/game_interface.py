import json

from tank_game.database import db, MatchFrame, MatchTanks, Match, TankFrame, FrameUpdates, Users
from .communicator import Communicator
from .game import Game

class GameInterface:
    def __init__(self, id):
        self.id = id

    def run(self):
        match = Match.query.filter_by(id = self.id).first()
        self.fn = 0

        self.communicator = Communicator(match.red_user.code, match.blue_user.code)
        self.communicator.start()

        self.game_engine = Game()
        self.game_engine.start_game(*self.communicator.recv_info())

        self.current_frame = self.game_engine.doframe([])
        self.serialize()

        while not self.game_engine.is_done():
            self.tick()
            self.serialize()

    def init_teams(self, red_team, blue_team):
        for colour, team in dict(red = red_team, blue = blue_team).items():
            for num, tank in enumerate(team):
                db.session.add(MatchTanks(
                    mid = self.id,
                    type = tank,
                    colour = colour,
                    number = num + 1
                ))

        db.session.commit()

    def tick(self):
        self.current_frame = self.game_engine.doframe(self.get_updates())
        self.fn += 1

    def get_updates(self):
        tanks = self.current_frame['tanks']

        red_info = [t for t in tanks if not t['invis'] or t['team'] == 'RED']
        blue_info = [t for t in tanks if not t['invis'] or t['team'] == 'BLUE']

        red_updates, blue_updates = self.communicator.send_info(red_info, blue_info)
        return red_updates + blue_updates

    def serialize(self):
        mf = MatchFrame(mid = self.id, frame_no = self.fn)
        db.session.add(mf)

        for tank in frame['tanks']:
            id = tank['id']
            team = tank['team']

            mt = MatchTanks.query.filter_by(mid = self.id, colour = tank['team'], number = tank['id']).first()
            db.session.add(mt)

            mt.frames.append(TankFrame(
                mfid = mf.id,
                mtid = mt.id,
                pos_x = tank['pos_x'],
                pos_y = tank['pos_y'],
                health = tank['health'],
                state = tank['state'],
                invis = tank['invis'],
                ability_cd = tank['ability_cd'],
                speed = tank['speed'],
                shileded = tank['shielded']
            ))

        for update in frame['updates']:
            id = update['id']
            team = update['team']

            mt = MatchTanks.query.filter_by(mid = self.id, colour = tank['team'], number = tank['id']).first()
            db.session.add(mt)

            mt.updates.append(FrameUpdates(
                mfid = mf.id,
                mtid = mt.id,
                action = update['action'],
                data = json.dumps(update['data'])
            ))

        db.session.commit()
