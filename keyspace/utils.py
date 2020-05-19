from flask import flash, redirect, url_for

import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.username is None:
            flash("You must be logged in to go there.", "warn")
            return redirect(url_for('front.login'))
        return view(**kwargs)

    return wrapped_view
