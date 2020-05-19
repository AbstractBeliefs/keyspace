from flask import render_template, session, redirect, request, flash, Blueprint, url_for
from passlib.hash import argon2
import sqlite3
from . import db, proofs

front_bp = Blueprint("front", __name__)

@front_bp.route("/")
def index():
    return render_template("front/index.html")

@front_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id", False):
        flash("You're already logged in!", "info")
        return redirect(url_for("front.index"))

    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]

        db_pass = db.query_db("SELECT id, password FROM users WHERE username = ?", (username,), True)
        if db_pass is None:
            flash("No such username: {}".format(username), "warn")
            return redirect(url_for("front.login"))

        if argon2.verify(password, db_pass["password"]):
            session.clear()
            session["user_id"] = db_pass["id"]
            flash("You're logged in as {}.".format(username), "info")
            return redirect(url_for("front.index"))
        else:
            flash("Incorrect password for {}.".format(username), "error")
            return redirect(url_for("front.login"))

    return render_template("front/login.html")


@front_bp.route("/logout")
def logout():
    session.clear()
    flash("You've logged out. Bye!", "info")
    return redirect(url_for("front.index"))

@front_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id", False):
        flash("You're already logged in!", "warn")
        return redirect(url_for("front.index"))

    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]

        if not username:
            flash("Username {} is not available".format(username), "warn")
            return redirect(url_for("front.register"))
        if not password:
            flash("Username {} is not available".format(username), "warn")
            return redirect(url_for("front.register"))

        try:
            passhash = argon2.hash(password)
            c = db.get_db().cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, passhash))
            db.get_db().commit()
        except sqlite3.IntegrityError:  # TODO: abstract this away, we shouldn't need to deal with sqlite ourselves here
            flash("Username {} is not available".format(username), "warn")
            return redirect(url_for("front.register"))

        flash("Registration complete, now log in!", "info")
        return redirect(url_for("front.login"))

    return render_template("front/register.html")
