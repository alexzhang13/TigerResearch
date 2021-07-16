from flask import Flask
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cas import CAS
from config import Config
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
import csv

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.auto_reload = True

# configs
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['CAS_SERVER'] = "ldap.cs.princeton.edu"
app.config['CAS_AFTER_LOGIN'] = 'route_root'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# For MySQL (later)
'''
db = MySQL(app)
app.config['MYSQL_HOST] = 
app.config['MYSQL_USER] = 
app.config['MYSQL_PASSWORD] = 
app.config['MYSQL_DB] = 
app.config['MYSQL_CURSORCLASS] = "DictCursor"
'''


CAS(app)
CORS(app)
Bootstrap(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Web Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/tigerresearch.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('TigerResearch Website')

from app import routes, errors
from app.models import models
from app.models.models import Professor

def init_db():
    db.drop_all()
    db.create_all()
    with open('db2.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['advising'] == "N":
                advising = False
            else:
                advising = True
            
            p = Professor(id=row['id'], name=row['name'], department=row['department'], 
            email=row['email'], website=row['website'], keywords=row['keywords'], 
            room=row['room'], advising=advising)

            db.session.add(p)
        db.session.commit()

init_db()