from flask import render_template, flash, redirect, url_for, request, jsonify
from sqlalchemy import create_engine
import json

from app import app
from app.models import models

@app.route("/", methods=["GET", "POST"])
def index():
    categories = [
        {'dep: COS'},
        {'dep:ORF'}
    ]
    return render_template("index.html", title='TigerResearch', categories=categories)

# TODO: Add login page
@app.route("/login")
def login():
    # form = LoginForm()
    return render_template("index.html", title='Log In')

@app.route("/livesearch", methods=["GET", "POST"])
def live_search():
    searchbox = request.form.get("text")
    res = models.Professor.query.filter_by(name=searchbox).all()
    res = models.Professor.query.all()
    return jsonify(json_list=[i.serialize for i in res])

def Convert(lst):
    resultproxy = lst
    new_dict = {}
    for prof in resultproxy:
        j_prof = json.dumps(prof)
        data = json.loads(j_prof)
        new_dict[prof.id] = data

    return jsonify(new_dict)