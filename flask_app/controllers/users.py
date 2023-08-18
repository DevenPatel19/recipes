from flask import flash, redirect, request, render_template, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt

from flask_app.config.mysql_connection import connect_to_mysql

bcrypt = Bcrypt(app)


@app.get("/")
def index_user():
    """Redirects the user to the form."""

    return render_template("login_create_user.html")


@app.post("/register")
def register_user():
    """Processes the Registration User form."""

    # validate the form
    # if valid, redirect user back to form
    if not User.registration_is_valid(request.form):
        return redirect("/")

    # look for user by email on form
    potential_user = User.get_by_email(request.form["email"])

    # is there is a user, redirect to form
    if potential_user:
        flash("Email in use please login")
        return redirect("/")
    print("User not found, please register.")

    # hash the users password (encrypt)
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }

    # save the user to the database
    user_id = User.create(data)

    # put the user's id into session
    session["user_id"] = user_id

    flash("Thanks for registering")

    # redirect to dashboard
    return redirect("/recipes/all")


@app.post("/login")
def login():
    """Processes the login form."""
    # validate form
    if not User.login_is_valid(request.form):
        return redirect("/")

    # check if user exists by email
    potential_user = User.get_by_email(request.form["email"])

    # if they don't exist, flash please register and redirect
    if not potential_user:
        flash("Invalid credentials.")
        return redirect("/")

    # check password if they exist
    user = potential_user

    # if password is wrong flash incorrect and redirect
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials.")
        return redirect("/")

    # put the user's id into session
    session["user_id"] = user.id

    # redirect to dashboard
    flash("Thanks for logging in")
    return redirect("/recipes/all")


@app.get("/logout")
def logout():
    """Clears session."""

    session.clear()
    return redirect("/")
