from flask import render_template
from app import app, forms


# Routes


@app.route("/")
def index():
    return render_template('index.html', home=True)


@app.route("/quick")
def quick():
    form = forms.QuickAddForm()
    return render_template(
        'quick.html', 
        title="Quick Add", 
        subtitle="Quickly add a video to the database.", 
        form=form
    )
