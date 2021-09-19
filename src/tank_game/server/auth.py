# -*- coding: utf-8 -*-

import jwt

from flask import request

from werkzeug.local import Local

from tank_game import app

from ..database import Users

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
    return jwt.encode(payload, app.secret_key, algorithm="HS256")


@app.before_request
def resolve_user():
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


@app.after_request
def set_user_cookie(response):
    if user:
        set_cookie(response, "user", make_jwt({"uid": user.id}))
    else:
        set_cookie(response, "user", "")
    return response


def set_cookie(response, key, val):
    response.set_cookie(key, val)
