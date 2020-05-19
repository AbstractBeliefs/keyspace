from flask import render_template, session, Blueprint, g
from . import db, proofs, utils

user_bp = Blueprint("user", __name__)

@user_bp.before_app_request
def populate_user_details():
    user_id = session.get("user_id")
    if user_id is None:
        g.username = None
    else:
        g.username = db.query_db("SELECT username FROM users WHERE id = ?", (user_id,), True)
        if g.username is not None:
            g.username = g.username["username"]

@user_bp.route("/me")
@utils.login_required
def user_profile():
    key_tree = proofs.get_proofs_for_user(session["user_id"])
    return render_template("front/me.html", key_tree=key_tree)
