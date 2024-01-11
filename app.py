import os, datetime
from flask import Flask, request, render_template, redirect
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

# == Your Routes Here ==


# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route("/index", methods=["GET"])
def get_index():
    return render_template("index.html")


# adding a space to the database through the webpage
@app.route("/list-space", methods=["POST"])
def submit_space():
    new_space = Space.create(
        name=request.form["name"],
        description=request.form["description"],
        price=request.form["price"],
        user_id=1,
    )
    Availability.create(
        start_date=request.form["start_date"],
        end_date=request.form["end_date"],
        space_id=new_space.id,
    )
    return redirect("/success")


# Page rendering


@app.route("/list-space", methods=["GET"])
def get_list_space():
    return render_template("list-space.html")


@app.route("/success", methods=["GET"])
def get_success():
    return render_template("success.html")


@app.route("/dashboard", methods=["GET"])
def get_dashboard():
    user_id = 1

    # Creates a list of dictionaries for bookings with booking details
    bookings = Booking.select().where(Booking.user_id == user_id)
    bookings_dicts = [booking.__dict__["__data__"] for booking in bookings]

    for booking in bookings_dicts:
        space = Space.select().where(Space.id == booking["space_id"]).first()
        if space != None:
            space_dict = space.__dict__["__data__"]
            del space_dict['id']
            booking.update(space_dict)

    # Creates a list of dictionaries for requests with request details
    requests = Booking.select().join(Space).where(Space.user_id == user_id)
    requests_dicts = [request.__dict__["__data__"] for request in requests]

    for request in requests_dicts:
        person = Space.select().where(Space.user_id == request["user_id"]).first()
        if person != None:
            person_dict = person.__dict__["__data__"]
            del person_dict['id']
            request.update(person_dict)

    return render_template("dashboard.html", bookings=bookings_dicts, requests=requests)


@app.route("/booking/<int:booking_id>", methods=["GET"])
def booking(booking_id):
    booking = Booking.select().join(Space).where(Booking.id == booking_id)
    print(booking)
    if booking:
        return render_template("booking.html", booking=booking)
    else:
        return "Booking not Found"


#
# @app.route("/approval/<int:booking_id>", methods=["GET"])
# def approval(booking_id):
#     user_id = 1 
#     requests = Booking.select().join(Space).where(Space.user_id == user_id)
#     requests_dicts = [request.__dict__["__data__"] for request in requests]

#     for request in requests_dicts:
#         person = Space.select().where(Space.user_id == request["user_id"]).first()
#         if person != None:
#             person_dict = person.__dict__["__data__"]
#             request.update(person_dict)
    

#     return render_template("approval.html", requests=requests, booking_id=booking_id)
    
@app.route("/approval/<int:booking_id>", methods=["GET"])
def approval(booking_id):
    request = Booking.select().join(Space).where(Booking.id == booking_id).first()
    request_dict = request.__dict__["__data__"]

    space = Space.select().where(Space.id == request.space_id).first()
    space_dict = space.__dict__["__data__"]
    del space_dict['id']
    request_dict.update(space_dict)
    
    print("REQUEST:", request_dict)
    return render_template("approval.html", request=request_dict)



@app.route("/approve/<int:booking_id>", methods=["POST"])
def approve(booking_id):
    booking = Booking.select().where(Booking.id == booking_id).first()

    if booking != None:
        booking.approved = True
        booking.response = True
        booking.save()

    return render_template("success.html")


# rejects a booking made on our space
@app.route("/reject/<int:booking_id>", methods=["POST"])
def reject(booking_id):
    booking = Booking.select().where(Booking.id == booking_id).first()

    if booking != None:
        booking.response = True
        booking.save()
    
    return render_template("success.html")




# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
