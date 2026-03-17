from .database import get_chats
from ..helpers.general import Colors
from flask import Blueprint, render_template, redirect, session, url_for

dashboard = Blueprint("dashboard", __name__)

print(Colors.GREEN+"dashboard"+Colors.BLUE+" initialized as a Blueprint.")

@dashboard.route("/dashboard", methods=["GET"])
def chat_base():
    if session.get("user.id") is None:
        print(Colors.YELLOW+"Redirect to login page.")
        return redirect(url_for("auth.login"))
    
    id = session.get("user.id")

    print(Colors.BLUE+"Loading conversations/chat rooms...")
    chats = get_chats(id)
    print(Colors.GREEN+"Chats loaded successfully...")
    return render_template("dashboard.html", conversations=chats)
