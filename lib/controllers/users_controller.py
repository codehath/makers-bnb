from flask import Blueprint, render_template, redirect, request, session
from lib.models.person import *
from lib.send_notifications import *
from lib.helper_methods import *

users_blueprint = Blueprint("users", __name__)


# Sign Up
@users_blueprint.route("/signup", methods=["GET"])
def get_signup():
    return render_template("users/new.html")


@users_blueprint.route("/signup", methods=["POST"])
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

    email_notification("signup", person)

    return redirect("/login")


# Login
@users_blueprint.route("/login", methods=["GET"])
def get_login():
    return render_template("users/login.html")


@users_blueprint.route("/login", methods=["POST"])
def post_login():
    email = request.form["email"]
    password = request.form["password"]
    person_registered = Person.select().where(Person.email == email).first()
    if person_registered == None:
        return render_template(
            "/messages/error.html", message="User does not exist, please try again."
        )
    if person_registered and person_registered.password == password:
        # Update Table - Reset all users logged_in values to False
        # reset = Person.update(logged_in=False)
        # reset.execute()
        # Update Table - Set logged_in value of the logging in user to True
        person_registered.logged_in = True
        person_registered.save()
        session["user_id"] = person_registered.id

        return redirect("/dashboard")
    else:
        return render_template(
            "/messages/error.html",
            message="Verify your username and password and try again.",
        )


# Log Out
@users_blueprint.route("/logout", methods=["GET"])
def get_logout():
    logged_in_user = get_logged_in_user()
    if logged_in_user:
        logged_in_user.logged_in = False
        logged_in_user.save()
        session.pop("user_id", None)
    return redirect("/spaces")
