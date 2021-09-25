from os import getenv

from flask import render_template, url_for, flash, redirect

from app import app, bcrypt
from app.forms import AuthForm, QuickAddForm
from app.settings import private_app


# Routes

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = AuthForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data)
        if bcrypt.check_password_hash(hashed_pass, getenv('PRIVATE_PASS')):
            flash('Access granted', 'success')
            return render_template('index.html', home=True)
        else:
            flash('Incorrect password', 'danger')
    if private_app:
        return render_template(
            'auth.html',
            home=True,
            title='Private access',
            subtitle='Log into a private database.',
            form=form
        )
    else:
        return render_template('index.html', home=True)


@app.route("/quick", methods=['GET', 'POST'])
def quick():
    form = QuickAddForm()
    if form.validate_on_submit():
        flash('Video submitted successfully', 'success')
        return redirect(url_for('index'))
    return render_template(
        'quick.html',
        title="Quick Add",
        subtitle="Quickly add a video to the database.",
        form=form
    )
