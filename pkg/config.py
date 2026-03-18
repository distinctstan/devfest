class General(object):
    APP_NAME="DevFest App"
    SQLALCHEMY_DATABASE_URI='postgresql+pymysql://devfest_db_x2af_user:y4sDsBVjrjKL1KBpkB04AURUdJBvHNL8@dpg-d6t652vkijhs73etmspg-a/devfest_db_x2af'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestConfig(General):
    DATABASE="devfest_db"

class LiveConfig(General):
    DATABASE="devfest_db"