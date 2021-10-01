from app import app
from flask import render_template


@app.errorhandler(404)
def err_404(error):
    return render_template('error.html', code=404, subtitle='An error occurred.', msg=error), 404


@app.errorhandler(403)
def err_403(error):
    return render_template('error.html', code=403, subtitle='An error occurred.', msg=error), 403


@app.errorhandler(500)
def err_500(error):
    return render_template('error.html', code=500, subtitle='An error occurred.', msg=error), 500
