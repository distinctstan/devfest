class General(object):
    APP_NAME="DevFest App"
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://freedb_devfest_user:hFyqa3G&XFE5Mf3@sql.freedb.tech:3306/freedb_devfest_db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestConfig(General):
    DATABASE="devfest_db"

class LiveConfig(General):
    DATABASE="devfest_db"