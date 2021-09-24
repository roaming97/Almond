from flask import Flask
from app import forms
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
from os import getenv

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = getenv("SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import tasks
tasks.create_db()

from app import routes
