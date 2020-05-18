from flask import render_template, session, redirect, request, flash
from passlib.hash import argon2
import sqlite3
from . import app, db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username", False):
        app.logger.info("Already logged in, redirecting")
        flash("You're already logged in!", "info")
        return redirect("/")

    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]

        db_pass = db.query_db("SELECT password FROM users WHERE username = ?", (username,), True)
        if db_pass is None:
            flash("No such username: {}".format(username), "warn")
            return redirect("/login")
        else:
            db_pass = db_pass[0]

        if argon2.verify(password, db_pass):
            session["username"] = username
            flash("You're logged in as {}.".format(username), "info")
            return redirect("/")
        else:
            flash("Incorrect password for {}.".format(username), "error")
            return redirect("/login")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session["username"] = False
    flash("You've logged out. Bye!", "info")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("username", False):
        app.logger.info("Already logged in, redirecting")
        flash("You're already logged in!", "warn")
        return redirect("/")

    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]

        if not username:
            flash("Username {} is not available".format(username), "warn")
            return redirect("/register")
        if not password:
            flash("Username {} is not available".format(username), "warn")
            return redirect("/register")

        try:
            passhash = argon2.hash(password)
            c = db.get_db().cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, passhash))
            db.get_db().commit()
        except sqlite3.IntegrityError:
            flash("Username {} is not available".format(username), "warn")
            return redirect("/register")

        app.logger.info("Registered with {}:{}".format(username, password))
        flash("Welcome to Keyspace, {}".format(username), "info")
        session["username"] = username
        return redirect("/")

    return render_template("register.html")
