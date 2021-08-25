from flask import render_template, request, session
from app import db
from app.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    if 'username' in session:
        return render_template('404.html', user=session['username']), 404
    else:
        return render_template('404.html', user=''), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if 'username' in session:
        return render_template('500.html', user=session['username']), 500
    else:
        return render_template('500.html', user=''), 500