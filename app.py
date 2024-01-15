import os
from datetime import datetime, timedelta
from flask import Flask, redirect, session, Response
from twilio.rest import Client
from werkzeug.routing import BaseConverter

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


def get_logged_in_user_or_redirect():
    user_id = session.get("user_id")
    print("user_id:", user_id)
    if user_id is None:
        print("Redirecting to login")
        return redirect("/login")
    print("Returning user")
    return Person.select().where(Person.id == user_id).first()


# Example usage in a controller method
@app.route("/example")
def example_controller():
    logged_in_user = get_logged_in_user_or_redirect()
    if isinstance(logged_in_user, Response):
        return logged_in_user

    # If get_logged_in_user_or_redirect() redirected, the following code won't execute
    if isinstance(logged_in_user, Person):  # Check if it's a Person instance
        # Your main logic here...
        return "This will only be reached if the user is logged in"

    return logged_in_user  # Return the redirect response


# Catch-all route to redirect undefined routes to whatever index redirects to
@app.route("/<path:undefined_route>")
def catch_all(undefined_route):
    return redirect("/")


# return render_template("print.html", print=dates)

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
