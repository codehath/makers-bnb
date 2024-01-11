import os, datetime
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection

from creds import *
from lib.person import *
from lib.availability import *
from lib.booking import *
from lib.space import *
from peewee import DoesNotExist
from flask_login import LoginManager


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
@app.route("/index", methods=["GET"])
def get_index():
    return render_template("index.html")

#SIGNUP ROUTES
@app.route("/signup", methods=["GET"])
def get_signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def post_signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    if password != request.form['confirm_password']:
        return f"Passwords do not match. Please try again."
    #Error - Parse in, Useful for Whole Application
        return redirect("/signup") 
    else:
        Person.create(name=name, email=email, password=password)
        return redirect("/login")

#LOGIN ROUTES
@app.route("/login", methods=["GET"])
def get_login():
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

            
        
# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
