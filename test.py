from app import create_app, init_db
from flask import session

my_app = create_app()
init_db(my_app)