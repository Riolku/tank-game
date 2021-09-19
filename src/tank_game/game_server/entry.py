from .game_interface import GameInterface

def run(id) -> None:
    gi = GameInterface(id)

    gi.run()
