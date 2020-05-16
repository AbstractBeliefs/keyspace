from flask import Flask
app = Flask(__name__)

from . import config, db
app.secret_key = config.secret_key
app.teardown_appcontext(db.cleanup)

from . import views
