import logging
from os import getenv
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_admin import Admin

from app import forms


app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = getenv("SECRET")
# PRODUCTION: Only enable this if the connection is strictly HTTPS, otherwise the site will not work correctly
# app.config['SESSION_COOKIE_SECURE'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app, template_mode='bootstrap4')

logging.basicConfig(
    filename='almond.log',
    filemode='w',
    format='%(levelname)s - %(message)s',
    level=logging.DEBUG
)
logging.getLogger(app.logger.name)

from app.settings import auto_db
from app.tasks import create_db
if auto_db:
    create_db()

from app import errors, routes
