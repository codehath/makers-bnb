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

#adding a space to the database through the webpage
@app.route("/submit-list-a-space", methods=["POST"])
def submit_a_space():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        new_space = Space.create(name=name, description=description, price=price, user_id=1)
        Availability.create(start_date=start_date, end_date=end_date, space_id=new_space.id)
        return redirect('/success')


  #Page rendering
    
@app.route("/list-a-space", methods=["GET"])
def get_list_a_space():
    return render_template("list_page.html")

@app.route("/success", methods=["GET"])
def get_success():
    return render_template("success_page.html")


@app.route("/dashboard", methods=["GET"])
def show_requests():
    user_id = 1 
    user_bookings = Booking.select().where(Booking.user_id == user_id)
    space_requests = Booking.select().join(Space, on=(Booking.space_id == Space.id)).where(Space.user_id == user_id).order_by(Booking.id).limit(300)
    return render_template("dashboard.html", user_bookings=user_bookings, space_requests=space_requests)

@app.route("/booking_details/<int:booking_id>", methods=['GET'])
def booking_details(booking_id):
    booking = Booking.select().join(Space).where(Booking.id == booking_id)
    print(booking)
    if booking:
        return render_template("booking_details.html", booking=booking)
    else:
        return "Booking not Found"

@app.route("/approval_page/<int:booking_id>", methods=["GET"])
def approval_page(booking_id):
    return render_template("approval_page.html" , booking_id=booking_id )

# @app.route("/confirm-a-space", methods=["POST"])
# def approve_a_space():
#     if request.method == "POST":
#         #approved = request.form['approved']
#         #response = request.form
#         Booking.update(approved=True, response=True)



# rejects a booking made on our space 
@app.route("/reject-a-space", methods=["POST"])
def refuse_a_space():
    if request.method == "POST":
        Booking.update(response = True)
        


    




# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
