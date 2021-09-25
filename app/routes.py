import os

from flask import render_template, url_for, flash, redirect
from app import app, forms, settings
from os import getenv


# Routes


@app.route("/", methods=['GET', 'POST'])
def index():
    form = forms.AuthForm()
    if form.validate_on_submit():
        if getenv('PRIVATE_PASS') == form.password.data:  # temporary check
            flash('Access granted', 'success')
            return render_template('index.html', home=True)
        else:
            flash('Incorrect password', 'danger')
    if settings.private_app:
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
    form = forms.QuickAddForm()
    if form.validate_on_submit():
        flash('Video submitted successfully', 'success')
        return redirect(url_for('index'))
    return render_template(
        'quick.html',
        title="Quick Add",
        subtitle="Quickly add a video to the database.",
        form=form
    )
