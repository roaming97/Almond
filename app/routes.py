from flask import render_template
from App import app

# Routes


@app.route("/")
def index(): return render_template('index.html')
