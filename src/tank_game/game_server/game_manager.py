from dmoj.utils.unicode import utf8bytes, utf8text
import json
import subprocess
from .sandboxed_executor import get_executor
from typing import Dict, List, Union

class GameManager:
    def __init__(self, red_source: str, blue_source: str):
        self.red = GameSubmission(red_source)
        self.blue = GameSubmission(blue_source)

    def start(self):
        self.red._start()
        self.blue._start()

    def kill(self):
        self.red.kill()
        self.blue.kill()

class GameSubmission:
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

    def send(self, data: Union[Dict, List]) -> None:
        self._proc.stdin.write(utf8bytes(json.dumps(data)) + b"\n")
        self._proc.stdin.flush()

    def recv(self) -> Union[Dict, List]:
        return json.loads(utf8text(self._proc.stdout.readline()))
