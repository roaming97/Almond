from os import getenv

from flask import render_template, url_for, flash, redirect, session, request, abort, send_file

from app import app, bcrypt, tasks, settings
from app.dictionaries import video_sorts
from app.forms import AuthForm, QuickAddForm, SearchForm, ManualAddForm
from app.models import Video


def access_denied(): return True if settings.private_app and "access" not in session else False


# Routes


@app.route("/", methods=['GET', 'POST'])
def index():
    if access_denied():
        return redirect(url_for('auth'))
    else:
        if Video.query.count() == 0:
            return render_template('index.html', home=True,
                                   private=settings.private_app, prevent=settings.prevent_resend,
                                   manual_add=settings.manual_add)

        page = request.args.get('page', 1, type=int)
        sort = request.args.get('sort', "newest-added", type=str)
        query = request.args.get('q', '', type=str) if settings.allow_search else None
        home = True

        s = sort if sort else session["current_sort"]
        data = Video.query.order_by(video_sorts.get(s, Video.id)).paginate(page=page,
                                                                           per_page=settings.videos_per_page)

        if query:
            home = False
            data = Video.query.filter(Video.title.contains(query)).order_by(video_sorts.get(s, Video.id)).paginate(
                page=1)

        session["current_sort"] = sort
        session["current_page"] = page

        form = SearchForm() if settings.allow_search else None
        if form.validate_on_submit():
            return redirect(url_for(
                'index',
                page=session['current_page'],
                sort=session["current_sort"],
                q=form.query.data
            ))

        def render_index(with_paginator=False):
            return render_template('index.html', home=home,
                                   private=settings.private_app, data=data,
                                   show_paginator=with_paginator, form=form,
                                   sorts=video_sorts, current_sort=session["current_sort"],
                                   prevent=settings.prevent_resend, manual_add=settings.manual_add)

        return render_index(with_paginator=True) if data.total > settings.videos_per_page else render_index()


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if not settings.private_app or "access" in session:
        return redirect(url_for('index', page=session["current_page"], sort=session["current_sort"]))
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
            form=form, prevent=settings.prevent_resend
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
            except Exception:
                abort(500)

        return render_template(
            'quick.html',
            title="Quick Add",
            subtitle="Quickly add a video to the database.",
            form=form
        )


@app.route("/manual", methods=['GET', 'POST'])
def manual():
    if access_denied():
        flash('Access denied', 'danger')
        return redirect(url_for('auth'))
    elif not settings.manual_add:
        flash('Manual adding is not enabled in this server', 'danger')
        return redirect(url_for('index', page=session["current_page"], sort=session["current_sort"]))
    else:
        form = ManualAddForm()
        if form.validate_on_submit():
            try:
                if tasks.manual_add(form=form):
                    flash('Video submitted successfully', 'success')
                    return redirect(url_for('index'))
            except Exception as e:
                flash(f'{e}', 'danger')
                return abort(500)

        return render_template(
            'manual.html',
            title="Manual Add",
            subtitle="Manually add a record to the database.",
            form=form, prevent=settings.prevent_resend
        )


@app.route("/download_db", methods=['GET'])
def download_db():
    if not access_denied() and 'admin' in session:
        return send_file('almond.db', as_attachment=True)
    else:
        abort(403)


@app.route("/logout", methods=['GET'])
def logout():
    if settings.private_app:
        tasks.clear_session_vars()
        flash('Logged out', 'info')
        return redirect(url_for('auth'))
    else:
        return redirect(url_for('index', page=session["current_page"], sort=session["current_sort"]))
