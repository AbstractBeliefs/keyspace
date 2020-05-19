from flask import Flask

def create_app():
    app = Flask(__name__)

    from . import config, db
    app.secret_key = config.secret_key
    db.init_db(app)

    from . import front, user
    app.register_blueprint(front.front_bp)
    app.register_blueprint(user.user_bp)

    return app
