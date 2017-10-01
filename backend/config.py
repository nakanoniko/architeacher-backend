JSON_AS_ASCII = False

SQLALCHEMY_DATABASE_URI = "postgresql://{username}:{password}@{hostname}/{databasename}".format(
    username="niko",
    password="QXJjaGlUZWFjaGVyUGFzc3dvcmQK",
    hostname="localhost",
    databasename="architeacher",
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = '$6$3pQZBLcMQjXz3JY5'

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False

SECRET_KEY = b'\xcf\xdd\xd8x,\xe6\x93\xd2\xa7\xcb\xa2x\xad\xe8CB \xd7\x12\x02\x02*\x8d\xbbCr\x9ewB\x15[' \
             b'\xb2\xbb\xc1\xb2\xd1 '
