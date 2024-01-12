import os, datetime
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection
from creds import MAILGUN_API_KEY, MAILGUN_DOMAIN, twilio_phone_number, account_sid, auth_token
import requests
from lib.send_texts import *
from twilio.rest import Client
# from flask_login import LoginManager
# from peewee import DoesNotExist

from creds import *
from lib.person import *
from lib.availability import *
from lib.booking import *
from lib.space import *

from lib.send_email import send_email, signup_email, space_created, approve_request, booking_denied, booking_request, booking_confirmed


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

# == Your Routes Here ==


# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route("/", methods=["GET"])
def get_index():
    return redirect("/spaces")

# SIGNUP ROUTES
@app.route("/signup", methods=["GET"])
def get_signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def post_signup():
    name = request.form['name']
    email = request.form['email']
    number = request.form['number']
    password = request.form['password']
    if password != request.form['confirm_password']:
        return f"Passwords do not match. Please try again."
        return redirect("/signup") 
    else:
        person = Person.create(name=name, email=email, password=password, number=number)

    # SEND WELCOME EMAIL FOR SIGNUP
    signup_email(person)
        
    return redirect("/login")
    

# LOGIN ROUTES
@app.route("/login", methods=["GET"])
def get_login():
    return render_template("login.html")

# LOG OUT ROUTE
@app.route("/logout", methods=["GET"])
def get_logout():
    global logged_in_user
    if logged_in_user:
        logged_in_user.logged_in = False
        logged_in_user.save()
        logged_in_user = None 
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def post_login():
    global logged_in_user
    email = request.form['email']
    password = request.form['password']
    person_registered = Person.select().where(Person.email == email).first()
    if person_registered == None:
        return render_template("error.html", message="User does not exist, please try again.")
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
        return render_template("error.html", message="Verify your username and password and try again.")


# NEW SPACE ROUTES
@app.route("/new-space", methods=["GET"])
def get_new_space():
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")
    return render_template("new-space.html")

@app.route("/new-space", methods=["POST"])
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
    # Notify the user about the created space
    space_created(logged_in_user, new_space)

    return redirect("/success")

# SUCCESS ROUTE
@app.route("/success", methods=["GET"])
def get_success():
    return render_template("success.html")


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
            del space_dict['id']
            booking.update(space_dict)

    # Creates a list of dictionaries for requests with request details
    requests = Booking.select().join(Space).where(
        (Space.user_id == user_id) & 
        (Booking.response == False)
        )
    requests_dicts = [request.__dict__["__data__"] for request in requests]

    for request in requests_dicts:
        person = Space.select().where(Space.user_id == request["user_id"]).first()
        if person != None:
            person_dict = person.__dict__["__data__"]
            del person_dict['id']
            request.update(person_dict)

    return render_template("dashboard.html", bookings=bookings_dicts, requests=requests)


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
    del space_dict['id']
    request_dict.update(space_dict)

    person = Person.select().where(Person.id == request.user_id).first()
    person_dict = person.__dict__["__data__"]
    person_dict["user_name"] = person_dict["name"]
    del person_dict["name"]
    del person_dict['id']
    request_dict.update(person_dict)
    
    return render_template("booking.html", request=request_dict)


# APPROVAL ROUTES
@app.route("/approval/<int:booking_id>", methods=["GET"])
def approval(booking_id):
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")
    
    request = Booking.select().join(Space).where(Booking.id == booking_id).first()
    request_dict = request.__dict__["__data__"]

    space = Space.select().where(Space.id == request.space_id).first()
    space_dict = space.__dict__["__data__"]
    del space_dict['id']
    del space_dict['user_id']
    request_dict.update(space_dict)

    person = Person.select().where(Person.id == request.user_id).first()
    person_dict = person.__dict__["__data__"]
    person_dict["user_name"] = person_dict["name"]
    del person_dict["name"]
    del person_dict['id']
    request_dict.update(person_dict)

    # Send email for booking request
    
    
    return render_template("approval.html", request=request_dict)

#Approving a Booking
@app.route("/approve/<int:booking_id>", methods=["POST"])
def approve(booking_id):
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")
    
    booking = Booking.select().where(Booking.id == booking_id).first()

    if booking != None:
        booking.approved = True
        booking.response = True
        booking.save()
        #Sending an email to the person who booked
        

        
#Sending text to the person who booked
    person = Person.select().where(Person.id == booking.user_id ).first()
    space = Space.select().where(Space.id == booking.space_id).first()
    requested_text_confirmed(person, space, booking)
    booking_confirmed(person, space, booking)
    

    return render_template("success.html")

@app.route("/reject/<int:booking_id>", methods=["POST"])
def reject(booking_id):
    global logged_in_user
    if logged_in_user == None:
        return redirect("/login")
    
    booking = Booking.select().where(Booking.id == booking_id).first()

    if booking != None:
        booking.response = True
        booking.save()

        # Fetch additional details (Person and Space)
        person = Person.select().where(Person.id == booking.user_id).first()
        space = Space.select().where(Space.id == booking.space_id).first()

        # Send a rejection email to the person who booked
        booking_denied(person, space, booking)
        requested_text_denied(person, space, booking)
    return render_template("success.html")


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))