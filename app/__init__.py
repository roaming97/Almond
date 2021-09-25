from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app import forms
from os import getenv

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = getenv("SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app.settings import auto_db

from app.tasks import create_db
if auto_db:
    create_db()

from app import routes
