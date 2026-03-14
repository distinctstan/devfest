class General(object):
    APP_NAME="DevFest App"
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root@localhost/devfest_db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestConfig(General):
    DATABASE="devfest_db"

class LiveConfig(General):
    DATABASE="devfest_db"