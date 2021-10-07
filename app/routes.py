from os import getenv

from flask import render_template, url_for, flash, redirect, session, request, abort

from app import app, bcrypt, tasks
from app.dictionaries import video_sorts
from app.forms import AuthForm, QuickAddForm, SearchForm
from app.models import Video
from app.settings import private_app, videos_per_page, allow_search, prevent_resend


def access_denied(): return True if private_app and "access" not in session else False


# Routes


@app.route("/", methods=['GET', 'POST'])
def index():
    if access_denied():
        return redirect(url_for('auth'))
    else:
        if Video.query.count() == 0:
            return render_template('index.html', home=True, private=private_app, prevent=prevent_resend)

        page = request.args.get('page', 1, type=int)
        sort = request.args.get('sort', "newest-added", type=str)
        query = request.args.get('q', '', type=str) if allow_search else None
        home = True

        s = sort if sort else session["current_sort"]
        data = Video.query.order_by(video_sorts.get(s, Video.id)).paginate(page=page, per_page=videos_per_page)

        if query:
            home = False
            data = Video.query.filter(Video.title.contains(query)).order_by(video_sorts.get(s, Video.id)).paginate(page=1)

        session["current_sort"] = sort
        session["current_page"] = page

        form = SearchForm() if allow_search else None
        if form.validate_on_submit():
            return redirect(
                url_for('index', page=session['current_page'], sort=session["current_sort"], q=form.query.data))

        def render_index(with_paginator=False):
            return render_template('index.html', home=home,
                                   private=private_app, data=data,
                                   show_paginator=with_paginator, form=form,
                                   sorts=video_sorts, current_sort=session["current_sort"],
                                   prevent=prevent_resend)

        return render_index(with_paginator=True) if data.total > videos_per_page else render_index()


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if not private_app or "access" in session:
        return redirect(url_for('index'))
    else:
        form = AuthForm()
        if form.validate_on_submit():
            hashed_pass = bcrypt.generate_password_hash(form.password.data)
            if bcrypt.check_password_hash(hashed_pass, getenv('PRIVATE_PASS')):
                tasks.init_session_vars()
                flash('Access granted', 'success')
                return redirect(url_for('index'))
            elif bcrypt.check_password_hash(hashed_pass, getenv('SECRET')):
                tasks.init_session_vars(admin=True)
                flash('Admin access granted', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
        return render_template(
            'auth.html',
            home=True,
            title='Private access',
            subtitle='Log into a private database.',
            form=form, prevent=prevent_resend
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
            try:
                if tasks.quick_add(form.url.data):
                    flash('Video submitted successfully', 'success')
                    return redirect(url_for('index'))
            except Exception as e:
                print(f'{e}')
                abort(500)

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
        session.pop("current_page", None)
        session.pop("current_sort", None)
        session.pop("admin", None)
        flash('Logged out', 'info')
        return redirect(url_for('auth'))
    else:
        return redirect(url_for('index'))
