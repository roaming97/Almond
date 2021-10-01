from os import getenv
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin

from app import forms

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = getenv("SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app)

from app.settings import auto_db

from app.tasks import create_db
if auto_db:
    create_db()

from app import errors, routes
