from dmoj import judgeenv
from dmoj.utils.unicode import utf8bytes

judgeenv.env["runtime"] = dict(python3="/usr/bin/python3")

from dmoj.executors import executors, load_executors

load_executors()  # Configure DMOJ executors
Executor = executors['PY3'].Executor

def get_executor(submission_source: str):
    with open("tank_game/game_server/api.py") as f:
        wrapper_code = f.read()

    e = Executor("tank-game", utf8bytes(wrapper_code))
    with open(e._file("submission.py"), "w") as f:
        f.write(submission_source)
    return e
