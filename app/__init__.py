from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import forms
from os import getenv

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = getenv("SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import settings
from app.tasks import create_db
if settings.auto_db:
    create_db()

from app import routes
