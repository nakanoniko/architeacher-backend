from flask import Flask
from flask_admin import Admin
from flask_security import SQLAlchemyUserDatastore, Security

from backend.database import db
from backend.models import User, Role

app = Flask(__name__)

app.config.from_pyfile('config.py')

db.init_app(app)

# connecting to user data store
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# setting app security
security = Security(app, user_datastore)

# initializing Flask-Admin
admin = Admin(
    app,
    base_template='/admin/my_master.html',
    template_mode='bootstrap3',
)

