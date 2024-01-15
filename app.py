import os
from datetime import datetime, timedelta
from flask import Flask, redirect, session, Response

# from lib.database_connection import get_flask_database_connection

from creds import *
from lib.person import *
from lib.availability import *
from lib.booking import *
from lib.space import *
from lib.send_notifications import *

# Import other controllers
from lib.controllers.users_controller import users_blueprint
from lib.controllers.dashboard_controller import dashboard_blueprint
from lib.controllers.spaces_controller import spaces_blueprint
from lib.controllers.bookings_controller import bookings_blueprint


# Create a new Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Replace with a secure secret key

# Register blueprints
app.register_blueprint(users_blueprint, url_prefix="/")
app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
app.register_blueprint(spaces_blueprint, url_prefix="/spaces")
app.register_blueprint(bookings_blueprint, url_prefix="/bookings")

# Define your Peewee database instance
db = PostgresqlDatabase(
    db_name,  # Your database name
    user=user,  # Your PostgreSQL username
    password=password,  # Your PostgreSQL password
    host=host,  # Your PostgreSQL host
)

# Connect to the database
db.connect()


# Index - Redirects to /spaces
@app.route("/", methods=["GET"])
def get_index():
    return redirect("/spaces")


# Catch-all route to redirect undefined routes to whatever index redirects to
@app.route("/<path:undefined_route>")
def catch_all(undefined_route):
    return redirect("/")


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
