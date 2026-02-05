from flask import Blueprint, request, render_template, redirect, session, url_for
from .database import fetch_user_by_name, create_user
import bcrypt

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
        
        user:tuple = fetch_user_by_name(name)

        if not user:
            return render_template("auth.html", error="Invalid User! Check your username.", mode="Login")
                
        """if not bcrypt.checkpw(password, user[2]):
            return render_template("auth.html", error="You did not key in the right password", mode="Login")""" # uncomment after building the register func
        
        if password != user[2]:
            return render_template("auth.html", error="You did not key in the right password", mode="Login")
        
        session["user.id"] = user[0]
        session["user.name"] = user[1]

        return redirect(url_for("dashboard")) # using room UI for now, dashboard UI coming up soon
    
    return render_template("auth.html", note="Register for a chat room using your username.", mode="Login")

@auth.route("/register", methods=["GET"])
def register():
    pass
