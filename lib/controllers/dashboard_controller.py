from flask import Blueprint, render_template, redirect, session, Response
from lib.person import *
from lib.space import *
from lib.booking import *
from lib.send_notifications import *
from lib.helper_methods import *

dashboard_blueprint = Blueprint("dashboard", __name__)


# Dashboard
@dashboard_blueprint.route("/", methods=["GET"])
def get_dashboard():
    logged_in_user = get_logged_in_user_or_redirect()
    if isinstance(logged_in_user, Response):
        return logged_in_user
    user_id = logged_in_user.id

    # Creates a list of dictionaries for bookings with booking details
    bookings = Booking.select().where(Booking.user_id == user_id)
    bookings_dicts = [booking.__dict__["__data__"] for booking in bookings]

    for booking in bookings_dicts:
        space = Space.select().where(Space.id == booking["space_id"]).first()
        if space != None:
            space_dict = space.__dict__["__data__"]
            del space_dict["id"]
            booking.update(space_dict)

    # Creates a list of dictionaries for requests with request details
    requests = (
        Booking.select()
        .join(Space)
        .where((Space.user_id == user_id) & (Booking.response == False))
    )
    requests_dicts = [request.__dict__["__data__"] for request in requests]

    for request in requests_dicts:
        person = Space.select().where(Space.user_id == request["user_id"]).first()
        if person != None:
            person_dict = person.__dict__["__data__"]
            del person_dict["id"]
            request.update(person_dict)

    return render_template(
        "dashboard.html",
        bookings=bookings_dicts,
        requests=requests,
        user=logged_in_user,
    )
