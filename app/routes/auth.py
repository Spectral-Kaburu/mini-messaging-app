from flask import Blueprint, request, render_template, redirect, session, url_for
from .database import fetch_user_by_name, create_user, check_pass_by_name
import bcrypt
import uuid

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["GET", "POST"])
def login():
    session.clear() # to allow for testing
    if request.method == "POST":
        name = request.form.get("username") # if 'username' not found null is returned
        password = request.form.get("password")

        if not name:
            return render_template("auth.html", error="Please enter a username", mode="Login")
        
        if not password:
            return render_template("auth.html", error="You did not key in your password", mode="Login")
        
        try:
            hashpw = str(bcrypt.hashpw(password, 10))
            user:tuple = check_pass_by_name(hashpw, name)
            if user:
                session["user.id"] = user[0]
                session["user.name"] = user[1]

                return redirect(url_for("chat_base")) # using room UI for now, dashboard UI coming up soon
        except Exception:
            return render_template("auth.html", error="Invalid Login credentials!!!", mode="Login")
    
    return render_template("auth.html", note="Register for a chat room using your username.", mode="Login")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username") # if 'username' not found null is returned
        password = request.form.get("password")

        if not name:
            return render_template("auth.html", error="Please enter a username", mode="Register")
        
        if not password:
            return render_template("auth.html", error="You did not key in a password", mode="Register")

        try:
            check = fetch_user_by_name(name)
            if check:
                return render_template("auth.html", error="Username already in use!!!", mode="Register")
        except Exception:

            hashpw = bcrypt.hashpw(password, 10)
            id = str(uuid.uuid4())

            user:tuple = create_user(id, name, hashpw)
        
            session["user.id"] = user[0]
            session["user.name"] = user[1]

            return redirect(url_for("chat_base")) # using room UI for now, dashboard UI coming up soon
    
    return render_template("auth.html", note="Register for a chat room using your username.", mode="Register")
