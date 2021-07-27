from app import create_app, init_db
from flask import session

session.clear()
my_app = create_app()