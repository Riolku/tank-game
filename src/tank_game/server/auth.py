# -*- coding: utf-8 -*-

import jwt

from flask import request

from werkzeug.local import Local

from tank_game import app

user_manager = Local()
user = user_manager("user")


class ExpiredJWT(Exception):
    pass


class InvalidJWT(Exception):
    pass


def set_user(obj):
    user_manager.user = obj


def verify_jwt(token):
    key = app.secret_key
    try:
        return jwt.decode(token, app.secret_key, algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureException:
        raise ExpiredJWT()
    except:
        raise InvalidJWT()


def make_jwt(payload):
    return jwt.encode(payload, app.secret_key, algorithm="HS256").decode(
        "utf-8"
    )


@app.before_request
def resolve_user():
    if request.endpoint == "static":
        return

    set_user(None)

    try:
        user_cookie = request.cookies.get("user", "")
        if user_cookie:
            token = verify_jwt(user_cookie)
            if "uid" not in token:
                return
            u = Users.query.filter_by(id=token["uid"]).first()
            if u:
                set_user(u)
    except:
        pass
