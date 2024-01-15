from flask import redirect, session
from datetime import datetime
from lib.person import *


def get_logged_in_user():
    user_id = session.get("user_id")
    if user_id:
        return Person.select().where(Person.id == user_id).first()
    return None


# By handling the redeirect here, if I wanted to change where the redirect points, only need to change code here
def get_logged_in_user_or_redirect():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    return Person.select().where(Person.id == user_id).first()


# Function to convert form date inputs into datetime objects...
# ...so that they can be compared against table DateFields
def date_conv(date):
    return datetime.strptime(date, "%Y-%m-%d")


def date_string(booking):
    # Adjust message if only 1 night
    date = f"from {booking.start_date} to {booking.end_date}"
    if booking.start_date == booking.end_date:
        date = f"on {booking.start_date}"

    return date
