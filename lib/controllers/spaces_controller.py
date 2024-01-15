from flask import Blueprint, render_template, redirect, request, session, Response
from datetime import datetime, timedelta
from lib.person import *
from lib.space import *
from lib.availability import *
from lib.booking import *
from lib.send_notifications import *
from lib.helper_methods import *

spaces_blueprint = Blueprint("spaces", __name__)


# SPACES ROUTES
@spaces_blueprint.route("/", methods=["GET"])
def spaces():
    logged_in_user = get_logged_in_user_or_redirect()
    if isinstance(logged_in_user, Response):
        return logged_in_user

    spaces = Space.select()
    return render_template("/spaces/index.html", spaces=spaces, user=logged_in_user)


@spaces_blueprint.route("/", methods=["POST"])
def spaces_date_range():
    logged_in_user = get_logged_in_user()

    # Join availability table to space table and only select spaces with availability between the dates entered in the form
    spaces = (
        Space.select()
        .join(Availability)
        .where(
            date_conv(request.form["avail-from"]) <= Availability.start_date
            and date_conv(request.form["avail-to"]) >= Availability.end_date
        )
    )
    return render_template("/spaces/index.html", spaces=spaces, user=logged_in_user)


# NEW SPACE ROUTES
@spaces_blueprint.route("/new", methods=["GET"])
def get_new_space():
    logged_in_user = get_logged_in_user_or_redirect()
    if isinstance(logged_in_user, Response):
        return logged_in_user
    return render_template("/spaces/new.html", user=logged_in_user)


@spaces_blueprint.route("/new", methods=["POST"])
def submit_space():
    logged_in_user = get_logged_in_user_or_redirect()
    if isinstance(logged_in_user, Response):
        return logged_in_user

    new_space = Space.create(
        name=request.form["name"],
        description=request.form["description"],
        price=request.form["price"],
        user_id=logged_in_user.id,
    )
    Availability.create(
        start_date=request.form["start_date"],
        end_date=request.form["end_date"],
        space_id=new_space.id,
    )

    email_notification("new_space", logged_in_user, new_space)

    return render_template(
        "/messages/success.html", message="Your space has been listed"
    )


# SPACE BOOKING ROUTES
@spaces_blueprint.route("/<int:id>", methods=["GET"])
def get_space(id):
    logged_in_user = get_logged_in_user()

    space = Space.select().where(Space.id == id).first()
    availability = Availability.select().where(Availability.space_id == id)
    bookings = Booking.select().where(Booking.space_id == id)

    # All the availabile dates
    avail_dates = []
    for dates in availability:
        if dates.start_date == dates.end_date:
            avail_dates.append(str(dates.start_date))
        else:
            avail_dates.append(
                [str(dates.start_date), str(dates.end_date + timedelta(days=1))]
            )

    booked_dates = []
    for dates in bookings:
        if dates.start_date == dates.end_date:
            booked_dates.append(str(dates.start_date))
        else:
            booked_dates.append(
                [str(dates.start_date), str(dates.end_date + timedelta(days=1))]
            )

    # return render_template("print.html", print=id)
    return render_template(
        "/spaces/show.html",
        space=space,
        booked_dates=booked_dates,
        id=id,
        user=logged_in_user,
    )

    return render_template("calendar.html", booked_dates=booked_dates)


@spaces_blueprint.route("/<int:id>", methods=["POST"])
def make_booking(id):
    logged_in_user = get_logged_in_user_or_redirect()
    if isinstance(logged_in_user, Response):
        return logged_in_user

    dates = request.form["datepicker"].split(" - ")
    booking = Booking.create(
        space_id=id, start_date=dates[0], end_date=dates[1], user_id=logged_in_user.id
    )

    space = Space.select().where(Space.id == id).first()
    host = Person.select().where(Person.id == space.user_id).first()
    email_notification("new_booking", logged_in_user, space, booking)
    email_notification("new_request", host, space, booking)
    sms_notification("request", host, space, booking)

    return redirect("/dashboard")
