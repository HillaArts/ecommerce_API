class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:HillaArts@HillaArts/test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key'
    JWT_SECRET_KEY = 'test_jwt_secret_key'
