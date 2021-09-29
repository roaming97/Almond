from os import getenv

from flask import render_template, url_for, flash, redirect, session

from app import app, bcrypt, tasks
from app.forms import AuthForm, QuickAddForm
from app.models import Video
from app.settings import private_app


# Routes


@app.route("/", methods=['GET', 'POST'])
def index():
    if private_app and "access" not in session:
        return redirect(url_for('auth'))
    else:
        data = Video.query.all()
        return render_template('index.html', home=True, private=private_app, data=data)


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if not private_app or "access" in session:
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


@app.route("/watch/<int:video_id>")
def watch(video_id):
    current_video = Video.query.get_or_404(video_id)
    return render_template(
        'template.html',
        title=current_video.title,
        subtitle="Watch a video."
    )


@app.route("/quick", methods=['GET', 'POST'])
def quick():
    if private_app and "access" not in session:
        flash('Access denied', 'danger')
        return redirect(url_for('auth'))
    else:
        form = QuickAddForm()
        if form.validate_on_submit():
            if tasks.get_video_info(form.url.data):
                flash('Video submitted successfully', 'success')
                return redirect(url_for('index'))
        return render_template(
            'quick.html',
            title="Quick Add",
            subtitle="Quickly add a video to the database.",
            form=form
        )


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if private_app:
        session.pop("access", None)
        flash('Logged out', 'info')
        return redirect(url_for('auth'))
    else:
        return redirect(url_for('index'))
