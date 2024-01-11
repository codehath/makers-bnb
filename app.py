import os  # , datetime
from datetime import datetime
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection

from creds import *
from lib.person import *
from lib.availability import *
from lib.booking import *
from lib.space import *


# Create a new Flask app
app = Flask(__name__)

# Define your Peewee database instance
db = PostgresqlDatabase(
    db_name,  # Your database name
    user=user,  # Your PostgreSQL username
    password=password,  # Your PostgreSQL password
    host=host,  # Your PostgreSQL host
)

# Connect to the database
db.connect()


# Function to convert form date inputs into datetime objects...
# ...so that they can be compared against table DateFields
def date_conv(date):
    return datetime.strptime(date, "%Y-%m-%d")


# == Your Routes Here ==


# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route("/index", methods=["GET"])
def get_index():
    return render_template("index.html")


@app.route("/spaces", methods=["GET"])
def spaces():
    spaces = Space.select()
    return render_template("spaces.html", spaces=spaces)


@app.route("/spaces", methods=["POST"])
def spaces_date_range():
    # Join availability table to space table and only select spaces with availability between the dates entered in the form
    spaces = (
        Space.select()
        .join(Availability)
        .where(
            date_conv(request.form["avail-from"]) <= Availability.start_date
            and date_conv(request.form["avail-to"]) >= Availability.end_date
        )
    )
    return render_template("spaces.html", spaces=spaces)


@app.route("/spaces/<int:id>", methods=["GET"])
def get_album(id):
    space = Space.select().where(id == id)

    # min_date should be today
    # max_date should be the last bookable date/month/year for that space

    # available_dates
    # All the availability dates

    # booked_dates
    # Get all bookings for this space
    # Get all dates for those bookings
    # store those in a list
    # if start date == end date, store start date
    # else store range as a pair

    booked_dates = [
        "2024-01-02",
        ["2024-01-06", "2024-01-11"],
        "2024-01-18",
        "2024-01-19",
        "2024-01-20",
        "2024-01-25",
        "2024-01-28",
    ]
    return render_template("space_cal.html", space=space[0], booked_dates=booked_dates)

    return render_template("calendar.html", booked_dates=booked_dates)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
