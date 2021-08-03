from flask import render_template, flash, redirect, url_for, request, jsonify, session, current_app
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
import json

from app import db
from app.main import bp
from app.models import models

import app.utils as utils
from cas import CASClient

cas_client = CASClient(
    version=3,
    service_url='http://localhost:5000/login?next=%2Fprofile',
    server_url='https://fed.princeton.edu/cas/login'
)

#@login_required
@bp.route("/", methods=["GET", "POST"])
def index():
    if 'username' in session:
        categories = utils.listify_file('app/static/assets/files/courses.txt')
        return render_template("index.html", title='TigerResearch', categories=categories, 
        user=session['username'])
    return redirect(url_for('main.login'))

# TODO: Add login page
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        # Already logged in
        return redirect(url_for('main.index'))
    
    next = request.args.get('next')
    ticket = request.args.get('ticket')
    if not ticket:
        # No ticket, the request come from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        current_app.logger.debug('CAS login URL: %s', cas_login_url)
        return redirect(cas_login_url)

    # There is a ticket, the request come from CAS as callback.
    # need call `verify_ticket()` to validate ticket and get user profile.
    current_app.logger.debug('ticket: %s', ticket)
    current_app.logger.debug('next: %s', next)

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    current_app.logger.debug(
        'CAS verify ticket response: user: %s, attributes: %s, pgtiou: %s', user, attributes, pgtiou)

    if not user:
        return 'Failed to verify ticket. <a href="/login">Login</a>'
    else:  # Login successfully, redirect according `next` query parameter.
        session['username'] = user
        user_id = models.User.query.filter_by(id=user).first()
        if user_id is None:
            user_id = models.User(netid=user, id=user, email=(user + "@princeton.edu"))
            db.session.add(user_id)
            db.session.commit()
        login_user(user_id)
        return redirect(url_for('main.index'))

@login_required
@bp.route('/profile')
def profile(method=['GET']):
    if 'username' in session:
        return 'Logged in as %s. <a href="/logout">Logout</a>' % session['username']
    return 'Login required. <a href="/login">Login</a>', 403

@login_required
@bp.route("/logout")
def logout():
    redirect_url = url_for('main.logout_callback', _external=True)
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    current_app.logger.debug('CAS logout URL: %s', cas_logout_url)
    logout_user()
    return redirect(cas_logout_url)

@bp.route('/logout_callback')
def logout_callback():
    # redirect from CAS logout request after CAS logout successfully
    session.pop('username', None)
    return 'Logged out from CAS. <a href="/login">Login</a>'

@login_required
@bp.route("/map")
def map():
    # form = LoginForm()
    return render_template("map.html", title='Map')

@login_required
@bp.route("/livesearch", methods=["GET", "POST"])
def live_search():
    searchbox = request.form.get("text")
    query = models.Professor.query
    query = query.filter(or_(*utils.get_filters(searchbox)))
    res = query.all()
    
    return jsonify(json_list=[i.serialize for i in res])

@login_required
@bp.route("/displayinfo", methods=["GET", "POST"])
def display_info():
    id = request.form.get("id")
    res = models.Professor.query.filter_by(netid=id).first()
    return jsonify(res.serialize)

@login_required
@bp.route('/professor/<netid>')
def get_professor(netid):
    if 'username' in session:
        res = models.Professor.query.filter_by(netid=netid).first()
        categories = utils.listify_file('app/static/assets/files/courses.txt')
        return render_template("index.html", title='TigerResearch', categories=categories, 
        user=session['username'], display=res)
    return redirect(url_for('main.login'))


@bp.route('/like/<prof_id>/<action>')
@login_required
def like_action(prof_id, action):
    prof = models.Professor.query.filter_by(id=prof_id).first_or_404()
    if action == 'like':
        current_user.like_prof(prof)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_prof(prof)
        db.session.commit()
    return redirect(request.referrer)

def Convert(lst):
    resultproxy = lst
    new_dict = {}
    for prof in resultproxy:
        j_prof = json.dumps(prof)
        data = json.loads(j_prof)
        new_dict[prof.id] = data

    return jsonify(new_dict)