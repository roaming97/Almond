from flask import render_template
from app import app

# Routes


@app.route("/")
def index(): return render_template('index.html')
