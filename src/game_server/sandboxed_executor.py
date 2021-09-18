from dmoj import judgeenv
from dmoj.utils.unicode import utf8bytes

judgeenv.env["runtime"] = dict(python3="/usr/bin/python3")

from dmoj.executors import executors, load_executors

load_executors()  # Configure DMOJ executors


def run_code(submission_source: str, **kwargs):
    # TODO: get manager template from a file
    manager_code = "import submission; submission.run()"
    e = Executor("tank-game", utf8bytes(manager_code))
    with open(e._file("submission.py"), "w") as f:
        f.write(submission_source)

    kwargs.setdefault("time", 30)
    kwargs.setdefault("memory", 262144)
    return e.launch(**kwargs)
