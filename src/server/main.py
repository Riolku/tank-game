import sys

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def serve_root():
    return "Hello, World!", 200


if __name__ == "__main__":
    arguments = sys.argv[1:]
    port = 5060
    debug = False
    while arguments:
        arg = arguments.pop(0)
        if arg == "-d" or arg == "--debug":
            debug = True
        elif arg == "-p" or arg == "--port":
            if arguments:
                rawport = arguments.pop(0)
                if rawport.isdigit():
                    port = int(rawport)
                else:
                    raise SystemExit(
                        "Argument after --port / -p must be a positive integer."
                    )
            else:
                raise SystemExit("There must be an argument after --port / -p")
    app.run(host="0.0.0.0", port=port, debug=debug)
