from .game_interface import GameInterface
from tank_game import celery

@celery.task
def run(id) -> None:
    gi = GameInterface(id)

    gi.run()
