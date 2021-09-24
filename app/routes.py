from flask import render_template, url_for, flash, redirect

from app import app, forms


# Routes


@app.route("/")
def index():
    return render_template('index.html', home=True)


@app.route("/quick", methods=['GET', 'POST'])
def quick():
    form = forms.QuickAddForm()
    if form.validate_on_submit():
        flash('Video submitted successfully.', 'success')
        return redirect(url_for('index'))
    return render_template(
        'quick.html',
        title="Quick Add",
        subtitle="Quickly add a video to the database.",
        form=form
    )
