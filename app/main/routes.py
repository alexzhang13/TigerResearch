from flask import render_template, flash, redirect, url_for, request, jsonify
from sqlalchemy import or_
import json

from app.main import bp
from app.models import models

import app.utils as utils

@bp.route("/", methods=["GET", "POST"])
def index():
    categories = utils.listify_file('app/static/assets/files/courses.txt')
    return render_template("index.html", title='TigerResearch', categories=categories)

# TODO: Add login page
@bp.route("/login")
def login():
    # form = LoginForm()
    return render_template("index.html", title='Log In')

# TODO: Add login page
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