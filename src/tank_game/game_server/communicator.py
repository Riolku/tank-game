from dmoj.utils.unicode import utf8bytes, utf8text
import json
import subprocess
from .sandboxed_executor import get_executor
from typing import Dict, List, Union, Tuple

JSON_Object = Union[Dict, List]


class Communicator:
    def __init__(self, red_source: str, blue_source: str):
        self.red = Submission(red_source)
        self.blue = Submission(blue_source)

    def start(self):
        self.red._start()
        self.blue._start()

    def kill(self):
        self.red.kill()
        self.blue.kill()

    def recv_info(self):
        return (self.red.recv(), self.blue.recv())

    def send_info(self, red_info: JSON_Object, blue_info: JSON_Object) -> Tuple[JSON_Object, JSON_Object]:
        self.red.send(red_info)
        self.blue.send(blue_info)

        return self.recv_info()


class Submission:
    def __init__(self, source: str):
        self._executor = get_executor(source)

    def _start(self) -> None:
        self._proc = self._executor.launch(
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            memory=262144,
            time=60
        )

    def kill(self) -> None:
        self._proc.kill()

    def send(self, data: JSON_Object) -> None:
        self._proc.stdin.write(utf8bytes(json.dumps(data)) + b"\n")
        self._proc.stdin.flush()

    def recv(self) -> JSON_Object:
        dt = utf8text(self._proc.stdout.readline())

        print(dt)
        return json.loads(dt)
