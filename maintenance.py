from app import create_app, init_db

my_app = create_app()

# re-initializes database with (possibly) updated information from csv
init_db(my_app)