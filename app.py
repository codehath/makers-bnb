import os
from datetime import datetime, timedelta
from flask import Flask, request, render_template, redirect
from twilio.rest import Client

from lib.database_connection import get_flask_database_connection

from creds import *
from lib.person import *
from lib.availability import *
from lib.booking import *
from lib.space import *
from lib.send_texts import *
from lib.send_notifications import *


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

logged_in_user = None


# Function to convert form date inputs into datetime objects...
# ...so that they can be compared against table DateFields
def date_conv(date):
    return datetime.strptime(date, "%Y-%m-%d")


# == Your Routes Here ==


# INDEX - Redirects to /spaces
@app.route("/", methods=["GET"])
def get_index():
    return redirect("/spaces")


# SIGNUP ROUTES
@app.route("/signup", methods=["GET"])
def get_signup():
    return render_template("users/new.html")


@app.route("/signup", methods=["POST"])
def post_signup():
    name = request.form["name"]
    email = request.form["email"]
    number = request.form["number"]
    password = request.form["password"]
    if password != request.form["confirm_password"]:
        return f"Passwords do not match. Please try again."
        return redirect("/signup")
    else:
        person = Person.create(name=name, email=email, password=password, number=number)

    # SEND WELCOME EMAIL FOR SIGNUP
    email_notification("signup", person)
    # signup_email(person)

    return redirect("/login")


# LOGIN ROUTES
@app.route("/login", methods=["GET"])
def get_login():
    return render_template("users/login.html")


@app.route("/login", methods=["POST"])
def post_login():
    global logged_in_user
    email = request.form["email"]
    password = request.form["password"]
    person_registered = Person.select().where(Person.email == email).first()
    if person_registered == None:
        return render_template(
            "/messages/error.html", message="User does not exist, please try again."
        )
    print(f"person registered: {person_registered} ")
    if person_registered and person_registered.password == password:
        # Update Table - Reset all users logged_in values to False
        reset = Person.update(logged_in=False)
        reset.execute()
        # Update Table - Set logged_in value of the logging in user to True
        person_registered.logged_in = True
        person_registered.save()
        logged_in_user = person_registered

        return redirect("/dashboard")
    else:
        return render_template(
            "/messages/error.html",
            message="Verify your username and password and try again.",
        )


# LOG OUT ROUTE
@app.route("/logout", methods=["GET"])
def get_logout():
    global logged_in_user
    if logged_in_user:
        logged_in_user.logged_in = False
        logged_in_user.save()
        logged_in_user = None
    return redirect("/spaces")


# DASHBOARD ROUTE
@app.route("/dashboard", methods=["GET"])
def get_dashboard():
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")
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


# VIEW BOOKING ROUTE
@app.route("/booking/<int:booking_id>", methods=["GET"])
def booking(booking_id):
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")

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
@app.route("/bookings/requests/<int:booking_id>", methods=["GET"])
def approval(booking_id):
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")

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
@app.route("/bookings/requests/approve/<int:booking_id>", methods=["POST"])
def approve(booking_id):
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")

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
@app.route("/bookings/requests/reject/<int:booking_id>", methods=["POST"])
def reject(booking_id):
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")

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


# SPACES ROUTES
@app.route("/spaces", methods=["GET"])
def spaces():
    global logged_in_user
    # return str(logged_in_user)

    spaces = Space.select()
    return render_template("/spaces/index.html", spaces=spaces, user=logged_in_user)


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
    return render_template("/spaces/index.html", spaces=spaces, user=logged_in_user)


# NEW SPACE ROUTES
@app.route("/spaces/new", methods=["GET"])
def get_new_space():
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")
    return render_template("/spaces/new.html", user=logged_in_user)


@app.route("/spaces/new", methods=["POST"])
def submit_space():
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")
    user_id = logged_in_user.id

    new_space = Space.create(
        name=request.form["name"],
        description=request.form["description"],
        price=request.form["price"],
        user_id=user_id,
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
@app.route("/spaces/<int:id>", methods=["GET"])
def get_space(id):
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


@app.route("/spaces/<int:id>", methods=["POST"])
def make_booking(id):
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


# Catch-all route to redirect undefined routes to spaces
@app.route("/<path:undefined_route>")
def catch_all(undefined_route):
    return redirect("/")


# return render_template("print.html", print=dates)

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
