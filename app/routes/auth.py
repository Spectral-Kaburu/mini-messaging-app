from .database import fetch_user_by_name, create_user
from ..helpers.general import Colors, hash_passwords, check_pass
from flask import Blueprint, request, render_template, redirect, session, url_for
import uuid

auth = Blueprint("auth", __name__, url_prefix="/auth")
print(Colors.GREEN+"auth"+Colors.BLUE+" initialized as a Blueprint.")

@auth.route("/login", methods=["GET", "POST"])
def login():
    session.clear() # to allow for testing
    if request.method == "POST":
        name = request.form.get("username") # if 'username' not found null is returned
        password = request.form.get("password")

        print(Colors.BLUE + "Currently processing login form...")

        if not name:
            print(Colors.YELLOW+"Please enter a username.")
            return render_template("auth.html", error="Please enter a username", mode="Login")
        
        if not password:
            print(Colors.YELLOW+"Please enter a password.")
            return render_template("auth.html", error="You did not key in your password", mode="Login")
        
        print(Colors.BLUE+"Checkng if credentials are valid...")
        user = fetch_user_by_name(name)
        if not user:
            print(Colors.RED+f"User with username ({name}) not found!!")
            return render_template("auth.html", error="Invalid login credentials!!!", mode="Login")
        print(Colors.GREEN+f"id: {user[0]}\nname: {user[1]}")
        hashed_pw = user[2]
        is_authenticated = check_pass(password, hashed_pw)
        if is_authenticated:
            session["user.id"] = user[0]
            session["user.name"] = user[1]
            print(Colors.GREEN+"Credentials validated and user logged in successfully!!!")
            return redirect(url_for('dashboard.chat_base')) # using room UI for now, dashboard UI coming up soon
        else:
            print(Colors.RED+"Invalid login credentials!!!")
            return render_template("auth.html", error="Invalid login credentials!!!", mode="Login")
    
    return render_template("auth.html", note="Register for a chat room using your username.", mode="Login")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username") # if 'username' not found null is returned
        password = request.form.get("password")

        print(Colors.BLUE + "Currently processing register form...")

        if not name:
            print(Colors.YELLOW+"Please enter a username.")
            return render_template("auth.html", error="Please enter a username", mode="Register")
        
        if not password:
            print(Colors.YELLOW+"Please key in your password.")
            return render_template("auth.html", error="You did not key in a password", mode="Register")

        print(Colors.BLUE+"Checking database for posted credentials...")
        check = fetch_user_by_name(name)
        if check:
            print(Colors.RED+"Username already in use!!!")
            return render_template("auth.html", error="Username already in use!!!", mode="Register")
        else:
            print(Colors.BLUE + "Creating user in database...")
            hashpw = hash_passwords(password)
            id = str(uuid.uuid4())

            user:tuple = create_user(id, name, hashpw)
            
            session["user.id"] = user[0]
            session["user.name"] = user[1]
            print(Colors.GREEN+"User successfully created and logged in!!!")

            return redirect(url_for('dashboard.chat_base')) # using room UI for now, dashboard UI coming up soon
    
    return render_template("auth.html", note="Register for a chat room using your username.", mode="Register")
