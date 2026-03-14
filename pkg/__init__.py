from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from pkg.config import TestConfig,LiveConfig
from pkg.devmodels import db

csrf = CSRFProtect()
def create_app():
    from pkg import devmodels
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")#read the config items defined in config.py
    app.config.from_object(LiveConfig) #instantiate an object of General, then read the config items from it

    db.init_app(app)
    migrate = Migrate(app,db)
    csrf.init_app(app)

    return app

app = create_app()

from pkg import devadmin_routes, devuser_routes, devforms, learn_routes