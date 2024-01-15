from flask import Blueprint, render_template, redirect, session
from datetime import timedelta
from lib.person import *
from lib.space import *
from lib.availability import *
from lib.booking import *
from lib.send_notifications import *

bookings_blueprint = Blueprint("bookings", __name__)


# VIEW BOOKING ROUTE
@bookings_blueprint.route("/<int:booking_id>", methods=["GET"])
def booking(booking_id):
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    logged_in_user = Person.select().where(Person.id == user_id).first()

    request = Booking.select().join(Space).where(Booking.id == booking_id).first()
    request_dict = request.__dict__["__data__"]

    space = Space.select().where(Space.id == request.space_id).first()
    space_dict = space.__dict__["__data__"]
    del space_dict["id"]
    request_dict.update(space_dict)

    person = Person.select().where(Person.id == request.user_id).first()
    person_dict = person.__dict__["__data__"]
    person_dict["user_name"] = person_dict["name"]
    del person_dict["name"]
    del person_dict["id"]
    request_dict.update(person_dict)

    return render_template(
        "/bookings/show.html", request=request_dict, user=logged_in_user
    )


# APPROVAL ROUTES
@bookings_blueprint.route("/requests/<int:booking_id>", methods=["GET"])
def approval(booking_id):
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    logged_in_user = Person.select().where(Person.id == user_id).first()

    request = Booking.select().join(Space).where(Booking.id == booking_id).first()
    request_dict = request.__dict__["__data__"]

    space = Space.select().where(Space.id == request.space_id).first()
    space_dict = space.__dict__["__data__"]
    del space_dict["id"]
    del space_dict["user_id"]
    request_dict.update(space_dict)

    person = Person.select().where(Person.id == request.user_id).first()
    person_dict = person.__dict__["__data__"]
    person_dict["user_name"] = person_dict["name"]
    del person_dict["name"]
    del person_dict["id"]
    request_dict.update(person_dict)

    return render_template(
        "/bookings/requests/show.html",
        request=request_dict,
        user=logged_in_user,
    )


# Approve a Booking
@bookings_blueprint.route("/requests/approve/<int:booking_id>", methods=["POST"])
def approve(booking_id):
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    logged_in_user = Person.select().where(Person.id == user_id).first()

    booking = Booking.select().where(Booking.id == booking_id).first()

    if booking != None:
        booking.approved = True
        booking.response = True
        booking.save()

    guest = Person.select().where(Person.id == booking.user_id).first()
    space = Space.select().where(Space.id == booking.space_id).first()

    email_notification("request_approved", logged_in_user, space, booking)
    sms_notification("booking_confirmed", guest, space, booking)
    email_notification("booking_confirmed", guest, space, booking)

    return render_template(
        "/messages/success.html",
        message="Your booking has been approved",
        user=logged_in_user,
    )


# Reject a Booking
@bookings_blueprint.route("/requests/reject/<int:booking_id>", methods=["POST"])
def reject(booking_id):
    user_id = session.get("user_id")
    if user_id == None:
        return redirect("/login")
    logged_in_user = Person.select().where(Person.id == user_id).first()

    booking = Booking.select().where(Booking.id == booking_id).first()

    if booking != None:
        booking.response = True
        booking.save()

        # Fetch additional details (Person and Space)
        guest = Person.select().where(Person.id == booking.user_id).first()
        space = Space.select().where(Space.id == booking.space_id).first()

        email_notification("booking_denied", guest, space, booking)
        sms_notification("booking_denied", guest, space, booking)

    return render_template(
        "/messages/success.html",
        message="You have successfully rejected the booking",
        user=logged_in_user,
    )
