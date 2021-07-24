from logging import disable
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dummy-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'profs.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['alzhang@princeton.edu']
    MAPBOX_KEY = os.environ.get('MAPBOX_KEY')
    TEMPLATES_AUTO_RELOAD = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    CAS_SERVER = "ldap.cs.princeton.edu"
    CAS_AFTER_LOGIN = 'route_root'
    MAPBOX_KEY = 'k.eyJ1IjoiYWx6aGFuZyIsImEiOiJja3JlYjdtYTk1a3pxMnRsMzU5cWZhbHpiIn0.uRUI-RC-5ebGhcKzC8bx2A'