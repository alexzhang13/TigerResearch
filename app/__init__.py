from app import utils

from flask import Flask, session
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
import csv

# For MySQL (later)
'''
db = MySQL(app)
app.config['MYSQL_HOST] = 
app.config['MYSQL_USER] = 
app.config['MYSQL_PASSWORD] = 
app.config['MYSQL_DB] = 
app.config['MYSQL_CURSORCLASS] = "DictCursor"
'''

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
cors = CORS()
login = LoginManager()

def init_db(app):
    print ("INIT DB")
    with app.app_context():
        db.drop_all()
        db.create_all()

        dep_to_color = {}
        dep_to_full = {}
        with open('app/static/assets/files/courses.txt', newline='') as f:
            lines = f.readlines()
            content = [x.split(',') for x in lines] 
            for d2c in content:
                dep_to_color[d2c[0]] = d2c[1]
                dep_to_full[d2c[0]] = d2c[2]

        with open('app/static/assets/files/data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                '''
                if (len(row['availability']) == 0): advising = True
                elif (row['availability'][0] == 'N' or row['availability'][0] == 'n'): advising = False
                else: advising = True
                '''
                advising = True
                h_index = row['h_index']
                citations = row['citations']
                if row['h_index'] == 'N/a': h_index=-1
                if row['citations'] == 'N/a': citations=-1
                if row['netid']=='N/a': continue

                p = Professor(netid=row['netid'], name=row['name'], department=row['department'], department_full=dep_to_full[row['department']],
                email=row['netid']+'@princeton.edu', citations=citations, department_color=dep_to_color[row['department']],
                hindex=h_index, picture=row['picture'], fingerprints=utils.listify_string(row['fingerprints']),
                projects=utils.listify_string(row['projects']), publications=utils.listify_string(row['research']),
                faculty=utils.listify_string(row['similar']), keywords=utils.get_keywords(row['fingerprints']), 
                website=utils.get_website(row['name'],row['netid'],row['department']), courses=utils.get_courses(row['classes']), 
                advising=advising)
                db.session.add(p)
            db.session.commit()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['SQLALCHEMY_ECHO'] = True
    app.config.from_object(config_class)
    app.jinja_env.auto_reload = True
    
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    login.login_view = 'main.login'

    with app.app_context():
        db.create_all()
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.forms import bp as forms_bp
    app.register_blueprint(forms_bp)

    if not app.debug and not app.testing:
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

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else: 
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

    return app

from app.models import models
from app.models.models import Professor