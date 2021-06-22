from flask import Flask
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cas import CAS
from config import Config

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

CAS(app)
CORS(app)
Bootstrap(app)

from app import routes, models

