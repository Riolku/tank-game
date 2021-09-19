# -*- coding: utf-8 -*-

import argon2, json, math, os, sys, time

from flask import flash, redirect, render_template, request

from .auth import *
from ..database import Users, db


def url_for_safe(*args, **kwargs):
    try:
        return url_for(*args, **kwargs)
    except:
        return ""


def render(*args, **kwargs):
    return render_template(
        *args, **kwargs, user=user, url_for_safe=url_for_safe
    )


@app.route("/")
def serve_root():
    return render("index.html"), 200


@app.route("/submit", methods=["GET"])
def serve_submit_page():
    if not user:
        return redirect("/"), 303
    else:
        return render("submit.html"), 200



@app.route("/submit", methods=["POST"])
def accept_submission():
    if request.form.get("switch") == "on":
        file = request.files["file"]
        code = file.read()
    else:
        code = request.form["code"]
    print(code)
    return "TODO", 200


@app.route("/signin", methods=["GET"])
def serve_signin_page():
    return render("signin.html"), 200


@app.route("/signin", methods=["POST"])
def handle_signin_request():
    username = request.form["username"]
    password = request.form["password"]

    u = Users.query.filter_by(username=username).first()
    if u is None:
        flash("Username and password don't match.", category="ERROR")
        return render("signin.html"), 200
    elif argon2.argon2_hash(password, username + "abcdefgh") != u.password:
        flash("Username and password don't match.", category="ERROR")
        return render("signin.html"), 200
    else:
        set_user(u)
        flash("Welcome back!", category="SUCCESS")
        return redirect("/"), 303


@app.route("/signup", methods=["GET"])
def serve_signup_page():
    return render("signup.html"), 200


@app.route("/signup", methods=["POST"])
def handle_signup_request():
    username = request.form["username"]
    password = request.form["password"]

    if password != request.form["rpassword"]:
        flash("Passwords don't match.", category="ERROR")
        return render("signup.html"), 200
    elif Users.query.filter_by(username=username).count() > 0:
        flash("Username is already taken.", category="ERROR")
        return render("signup.html"), 200
    else:
        user = Users(
            username=username,
            password=argon2.argon2_hash(password, username + "abcdefgh"),
        )
        db.session.add(user)
        db.session.commit()
        set_user(user)
        flash("Welcome! Your account has been created.", category="SUCCESS")
        return redirect("/"), 303


@app.route("/signout")
def handle_signout_request():
    set_user(None)
    flash("Goodbye!", category="SUCCESS")
    return redirect("/"), 303


@app.route("/replay-viewer/<int:match>")
def replay_viewer(match):
    # TODO get actual match data
    return render("replay-viewer.html", match=match, frames=1), 200


@app.route("/match-data/<int:match>")
def match_data(match):
    # TODO get actual match data
    return json.dumps(
        [
            [
                [[390, 10], [410, 10], [410, 110], [390, 110]],
                [[390, 590], [410, 590], [410, 490], [390, 490]],
            ],
            ["hyper-neutrino", "riolku"],
            [
                ["repair", "artillery", "assassin", "shield", "shield"],
                ["kamikaze", "scout", "mortar", "hack", "shield"],
            ],
            [
                [
                    [
                        [
                            100,
                            100,
                            100,
                            0,
                            -1,
                            0,
                            1,
                            [],
                        ],  # repair the artillery
                        [
                            100,
                            200,
                            100,
                            0,
                            0,
                            0,
                            -1,
                            [],
                        ],  # fire directly to the east
                        [100, 300, 100, 0, -1, 0, 0, ["speedy"]],  # gain MS
                        [100, 400, 100, 100, -1, 0, 0, []],  # shield around
                        [
                            100,
                            500,
                            100,
                            0,
                            math.pi / 2,
                            0,
                            -1,
                            [],
                        ],  # fire directly to the north
                    ],
                    [
                        [700, 100, 100, 0, -1, 0, 0, []],  # explode
                        [
                            700,
                            200,
                            100,
                            0,
                            -1,
                            0,
                            0,
                            ["invisible"],
                        ],  # go invisible
                        [
                            700,
                            300,
                            100,
                            0,
                            -1,
                            0,
                            [500, 300],
                            ["hacked"],
                        ],  # throw bomb at center
                        [
                            700,
                            400,
                            100,
                            0,
                            math.pi,
                            0,
                            -1,
                            [],
                        ],  # fire directly to the west
                        [
                            700,
                            500,
                            100,
                            0,
                            math.pi * 3 / 2,
                            0,
                            -1,
                            [],
                        ],  # fire directly to the south
                    ],
                    [-1, 100],
                ],
                [
                    [
                        [
                            100,
                            110,
                            100,
                            0,
                            math.pi * 3 / 4,
                            0,
                            1,
                            [],
                        ],  # repair the artillery
                        [
                            100,
                            200,
                            100,
                            0,
                            0,
                            0,
                            -1,
                            ["empowered"],
                        ],  # fire directly to the east
                        [100, 300, 100, 0, -1, 0, 0, ["speedy"]],  # gain MS
                        [100, 400, 100, 100, -1, 0, 0, []],  # shield around
                        [
                            100,
                            500,
                            100,
                            0,
                            math.pi / 2,
                            0,
                            -1,
                            [],
                        ],  # fire directly to the north
                    ],
                    [
                        0,  # explode
                        [
                            700,
                            200,
                            100,
                            0,
                            -1,
                            0,
                            0,
                            ["invisible"],
                        ],  # go invisible
                        [
                            700,
                            300,
                            100,
                            0,
                            -1,
                            0,
                            -1,
                            [],
                        ],
                        [
                            700,
                            400,
                            100,
                            0,
                            math.pi,
                            0,
                            -1,
                            [],
                        ],  # fire directly to the west
                        [
                            700,
                            500,
                            100,
                            0,
                            math.pi * 3 / 2,
                            0,
                            -1,
                            [],
                        ],  # fire directly to the south
                    ],
                    [-1, 90],
                ],
            ],
        ]
    )


@app.errorhandler(404)
def not_found(e):
    return render("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render("500.html"), 500
