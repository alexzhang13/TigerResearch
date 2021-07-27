from flask import render_template, flash, redirect, url_for, request, jsonify, session, current_app
from sqlalchemy import or_
import json

from app.main import bp
from app.models import models

import app.utils as utils
from cas import CASClient

cas_client = CASClient(
    version=3,
    service_url='http://localhost:5000/login?next=%2Fprofile',
    server_url='https://fed.princeton.edu/cas/login'
)

@bp.route("/", methods=["GET", "POST"])
def index():
    if 'username' in session:
        categories = utils.listify_file('app/static/assets/files/courses.txt')
        return render_template("index.html", title='TigerResearch', categories=categories, user=session['username'])
    return redirect(url_for('main.login'))

# TODO: Add login page
@bp.route("/login")
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
        return redirect(url_for('main.index'))

@bp.route('/profile')
def profile(method=['GET']):
    if 'username' in session:
        return 'Logged in as %s. <a href="/logout">Logout</a>' % session['username']
    return 'Login required. <a href="/login">Login</a>', 403

@bp.route("/logout")
def logout():
    redirect_url = url_for('main.logout_callback', _external=True)
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    current_app.logger.debug('CAS logout URL: %s', cas_logout_url)

    return redirect(cas_logout_url)

@bp.route('/logout_callback')
def logout_callback():
    # redirect from CAS logout request after CAS logout successfully
    session.pop('username', None)
    return 'Logged out from CAS. <a href="/login">Login</a>'

@bp.route("/map")
def map():
    # form = LoginForm()
    return render_template("map.html", title='Map')

@bp.route("/livesearch", methods=["GET", "POST"])
def live_search():
    searchbox = request.form.get("text")
    # res = models.Professor.query.filter(models.Professor.__ts_vector__.match(searchbox)).all()
    query = models.Professor.query
    query = query.filter(or_(*utils.get_filters(searchbox)))
    res = query.all()
    
    return jsonify(json_list=[i.serialize for i in res])

@bp.route("/displayinfo", methods=["GET", "POST"])
def display_info():
    id = request.form.get("id")
    res = models.Professor.query.filter_by(netid=id).first()
    return jsonify(res.serialize)

def Convert(lst):
    resultproxy = lst
    new_dict = {}
    for prof in resultproxy:
        j_prof = json.dumps(prof)
        data = json.loads(j_prof)
        new_dict[prof.id] = data

    return jsonify(new_dict)