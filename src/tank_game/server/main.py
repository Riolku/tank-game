# -*- coding: utf-8 -*-

import argon2, json, math, os, sys, time

from sqlalchemy.orm import joinedload

from flask import flash, redirect, render_template, request

from .auth import *
from ..database import (
    Match,
    MatchFrame,
    TankFrame,
    MatchTanks,
    FrameUpdates,
    Users,
    db,
)


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
        return render("submit.html", code=user.code or ""), 200


@app.route("/submit", methods=["POST"])
def accept_submission():
    if not user:
        flash("You are not logged in.", category="ERROR")
        return redirect("/"), 303

    if request.form.get("switch") == "on":
        file = request.files["file"]
        code = file.read()
    else:
        code = request.form["code"]
    user.code = code
    db.session.commit()
    flash("Code submitted!", category="SUCCESS")
    return render("submit.html", code=user.code or ""), 200


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


@app.route("/userlist")
def serve_userlist():
    return render(
        "userlist.html", users=Users.query.filter(Users.code != None).all()
    )


@app.route("/challenge/<int:id>")
def challenge(id):
    if not user:
        flash("You must be signed in!", category="ERROR")
        return redirect("/signin"), 303
    else:
        u = Users.query.filter_by(id=id).first()
        if u is None:
            flash("Opponent does not exist!", category="ERROR")
            return redirect("/userlist"), 303
        elif user.id == id:
            flash("You cannot challenge yourself!", category="ERROR")
            return redirect("/userlist"), 303
        elif not u.code.strip():
            flash(
                "You cannot challenge someone who hasn't submitted code!",
                category="ERROR",
            )
            return redirect("/userlist"), 303
        else:
            return render("challenge.html", match=0, target=u), 200


@app.route("/replay-viewer/<int:mid>")
def replay_viewer(mid):
    match = Match.query.filter_by(id=mid).first_or_404()
    return (
        render(
            "replay-viewer.html",
            match=match,
            frames=MatchFrame.query.filter_by(mid=mid).count(),
        ),
        200,
    )


@app.route("/match-data/<int:mid>")
def match_data(mid):
    match = Match.query.filter_by(id=mid).first()
    red_tanks = MatchTanks.query.filter_by(mid=match.id, colour="RED").all()
    blue_tanks = MatchTanks.query.filter_by(mid=match.id, colour="BLUE").all()

    match_frames = (
        MatchFrame.query.filter_by(mid=mid)
        .order_by(MatchFrame.frame_no)
        .options(joinedload("tank_frames"), joinedload("frame_updates"))
        .all()
    )

    def format_frame_for_team(tanks, enemy, f):
        ret = []

        for t in tanks:
            tf = TankFrame.query.with_parent(f).filter_by(mtid=t.id).first()
            updates = (
                FrameUpdates.query.with_parent(f).filter_by(mtid=t.id).all()
            )

            angle = -1
            ability = -1

            for update in updates:
                if update.action == "FIRE":
                    target = enemy[int(update.data)]
                    target_frame = (
                        TankFrame.query.with_parent(f)
                        .filter_by(mtid=target.id)
                        .first()
                    )
                    angle = math.atan2(
                        target_frame.pos_y - tf.pos_y,
                        target_frame.pos_x - tf.pos_x,
                    )
                elif update.action == "ABILITY":
                    if tf.tank.type in [
                        "artillery",
                        "assassin",
                        "shield",
                        "kamikaze",
                        "scout",
                    ]:
                        ability = 0
                    elif tf.tank.type == "mortar":
                        ability = json.loads(update.data)
                    elif tf.tank.type in ["repair", "hack"]:
                        ability = int(update.data)

            ret.append(
                [
                    tf.pos_x,
                    tf.pos_y,
                    tf.health,
                    angle,
                    tf.ability_cd,
                    ability,
                    [y for x, y in [(tf.shielded, "shielded")] if x],
                ]
            )

        return ret

    return json.dumps(
        [
            [],
            [match.red_user.username, match.blue_user.username],
            [
                [rt.type for rt in red_tanks],
                [bt.type for bt in blue_tanks],
            ],
            [
                [
                    format_frame_for_team(red_tanks, blue_tanks, f),
                    format_frame_for_team(blue_tanks, red_tanks, f),
                ]
                for f in match_frames
            ],
        ]
    )


@app.route("/users")
def handle_users():
    users = Users.query.filter(Users.code != None).all()
    print(users)
    return render("users.html", users=users), 200


@app.route("/battle", methods=["POST"])
def handle_battle():
    pass


@app.errorhandler(404)
def not_found(e):
    return render("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render("500.html"), 500
