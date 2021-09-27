from os import getenv

from flask import render_template, url_for, flash, redirect, session

from app import app, bcrypt
from app.forms import AuthForm, QuickAddForm
from app.settings import private_app


# Routes


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if private_app and "access" not in session:
        return redirect(url_for('auth'))
    else:
        return render_template('index.html', home=True)


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if "access" in session or not private_app:
        return redirect(url_for('index'))
    else:
        form = AuthForm()
        if form.validate_on_submit():
            hashed_pass = bcrypt.generate_password_hash(form.password.data)
            if bcrypt.check_password_hash(hashed_pass, getenv('PRIVATE_PASS')):
                session["access"] = True
                flash('Access granted', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
        return render_template(
                'auth.html',
                home=True,
                title='Private access',
                subtitle='Log into a private database.',
                form=form
            )


@app.route("/quick", methods=['GET', 'POST'])
def quick():
    if private_app and "access" not in session:
        flash('Access denied', 'danger')
        return redirect(url_for('auth'))
    else:
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
