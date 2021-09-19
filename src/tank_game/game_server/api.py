import json
import submission

print(json.dumps(submission.get_tanks()))

class Tank:
    def __init__(self, dt):
        self.__dict__.update(**dt)

while 1:
    data = json.loads(input())

    print(json.dumps(submission.run_frame([Tank(tk) for tk in data])))
