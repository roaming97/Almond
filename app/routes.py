from flask import render_template
from app import app

dummy = [
    {
        'title': 'sample video 1',
        'author': 'myself',
        'description': 'my video',
        'date': 'January 1, 2009'
    },
    {
        'title': 'sample video 2',
        'author': 'myself again',
        'description': 'my second video',
        'date': 'October 15, 2012'
    },
]


# Routes


@app.route("/")
def index(): return render_template('index.html')
