import json
import submission

print(json.dumps(submission.get_tanks()))

while 1:
    data = json.loads(input())

    print(json.dumps(submission.run_frame(data)))
