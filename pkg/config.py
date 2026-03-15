class General(object):
    APP_NAME="DevFest App"
    SQLALCHEMY_DATABASE_URI='postgresql://devfest_db_i26t_user:G6xc0zrYQqOTAlnXtvxpGpasUiobuaNS@dpg-d6qvh39aae7s739nnq2g-a/devfest_db_i26t'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestConfig(General):
    DATABASE="devfest_db"

class LiveConfig(General):
    DATABASE="devfest_db"