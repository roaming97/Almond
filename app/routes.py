from flask import render_template
from datetime import datetime
from app import app

dummy = [
    {
        'title': 'sample video 1',
        'author': 'myself',
        'description': 'my video',
        'date': datetime.strptime("01/01/2009","%m/%d/%Y").strftime('%m/%d/%Y')
    },
    {
        'title': 'sample video 2',
        'author': 'myself again',
        'description': 'my second video',
        'date': datetime.strptime("11/04/2012","%m/%d/%Y").strftime('%m/%d/%Y')
    },
]


# Routes


@app.route("/")
def index(): return render_template('index.html')
