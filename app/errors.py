from app import app
from flask import render_template


def r_error(err, code: int):
    return render_template('error.html',
                           code=str(err).split(":")[0],
                           subtitle='An error occurred.',
                           msg=str(err).split(":")[1]), code


@app.errorhandler(404)
def err_404(error): return r_error(error, 404)


@app.errorhandler(403)
def err_403(error): return r_error(error, 403)


@app.errorhandler(413)
def err_413(error): return r_error(error, 413)


@app.errorhandler(500)
def err_500(error): return r_error(error, 500)
