from dmoj import judgeenv

judgeenv.env['runtime'] = dict(python3 = '/usr/bin/python3')

from dmoj.executors import executors, load_executors

load_executors()

def run_code(source : bytes, **kwargs):
    kwargs.setdefault('time', 30)
    kwargs.setdefault('memory', 262144)

    e = Executor('tank-game', source)

    # TODO: get manager template from a file
    manager_code = "import submission; submission.run()"

    with open(e._file('submission.py'), "w") as f:
        f.write(manager_code)

    return e.launch(**kwargs)
