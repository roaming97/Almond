from os import getenv

from flask import render_template, url_for, flash, redirect, session, request

from app import app, bcrypt, tasks
from app.forms import AuthForm, QuickAddForm
from app.models import Video
from app.settings import private_app, videos_per_page


def access_denied():
    return True if private_app and "access" not in session else False

# Routes


@app.route("/", methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', "newest-added", type=str)
    if access_denied():
        return redirect(url_for('auth'))
    else:

        video_sorts = {
            'newest-added': Video.id.desc(),
            'oldest-added': Video.id,
            'newest': Video.date.desc(),
            'oldest': Video.date,
        }

        if sort:
            data = Video.query.order_by(video_sorts.get(sort, Video.id)).paginate(page=page, per_page=videos_per_page)
        else:
            data = Video.query.order_by(video_sorts.get(session["current_sort"], Video.id))\
                .paginate(page=page, per_page=videos_per_page)

        session["current_sort"] = sort
        session["current_page"] = page

        if data.total > videos_per_page:
            return render_template('index.html', home=True,
                                   private=private_app, data=data,
                                   show_paginator=True, sorts=video_sorts, current_sort=session["current_sort"])
        else:
            return render_template('index.html', home=True,
                                   private=private_app, data=data,
                                   sorts=video_sorts, current_sort=session["current_sort"])


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if not private_app or "access" in session:
        return redirect(url_for('index'))
    else:
        form = AuthForm()
        if form.validate_on_submit():
            hashed_pass = bcrypt.generate_password_hash(form.password.data)
            if bcrypt.check_password_hash(hashed_pass, getenv('PRIVATE_PASS')):
                session["current_page"] = 1
                session["current_sort"] = "newest_added"
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
    if access_denied():
        flash('Access denied', 'danger')
        return redirect(url_for('auth'))
    else:
        current_video = Video.query.get_or_404(video_id)
        return render_template(
            'video.html',
            title=current_video.title,
            subtitle="Watch a video.",
            video_data=current_video
        )


@app.route("/quick", methods=['GET', 'POST'])
def quick():
    if access_denied():
        flash('Access denied', 'danger')
        return redirect(url_for('auth'))
    else:
        form = QuickAddForm()
        if form.validate_on_submit():
            if tasks.quick_add(form.url.data):
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
