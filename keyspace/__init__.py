from flask import Flask

def create_app():
    app = Flask(__name__)

    from . import config, db
    app.secret_key = config.secret_key
    db.init_db(app)

    from . import front
    app.register_blueprint(front.front_bp)

    return app
