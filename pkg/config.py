class General(object):
    APP_NAME="DevFest App"
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://avnadmin:AVNS_0DGOppAMKgvy63mM3Cg@mysql-63c54de-stantechsolutions20-433a.k.aivencloud.com:22971/devfestdb?ssl-mode=REQUIRED'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestConfig(General):
    DATABASE="devfest_db"

class LiveConfig(General):
    DATABASE="devfest_db"