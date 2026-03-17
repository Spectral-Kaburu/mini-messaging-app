from .routes.auth import auth
from .routes.database import send_msg, get_mesgs
from .routes.dashboard import dashboard
#from .routes.conversations import conversations
from .helpers.general import Colors
from flask_socketio import SocketIO, join_room, leave_room, send
from flask import Flask, session, render_template
from http.client import HTTPException
import uuid
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "messaging_app"
socketio = SocketIO(app)
app.register_blueprint(auth)
app.register_blueprint(dashboard)
#app.register_blueprint(conversations)

# Custom 404 handler
@app.errorhandler(404)
def page_not_found(e):
    print(Colors.RED+f"{e}")
    return render_template('404.html'), 404

# Custom 500 handler (and other 5xx errors)
@app.errorhandler(500)
def internal_server_error(e):
    print(Colors.RED+f"{e}")
    return render_template('500.html'), 500

# Optional: Catch-all for other HTTP errors (400, 403, 429, etc.)
@app.errorhandler(Exception)
def handle_exception(e):
    print(Colors.RED+f"{e}")
    # Only handle HTTP exceptions here (avoid catching programming errors twice)
    if isinstance(e, HTTPException):
        code = e.code if hasattr(e, 'code') else 500
        return render_template('500.html'), code  # or a generic error template
    # Let other exceptions bubble up (for debugging / logging middleware)
    raise

print(Colors.BLUE+"Initialization process complete!")

def sanitize(mesg:str, chat_id:str, user_id:str)->dict:
    msg_id = str(uuid.uuid4())
    message = {
        "msg_id": msg_id,
        "chat_id": chat_id,
        "content": mesg,
        "sender_id": user_id,
    }
    return message

@socketio.on("message")
def message(msg):
    chat_id = session.get("conversation.id")
    user_id = session.get("user.id")
    message = sanitize(msg, chat_id, user_id)
    send(message, to=chat_id)
    try:
        send_msg(message)
    except Exception:
        print(Colors.RED+"Inserting message into database failed!!")


@socketio.on("connect")
def connect(auth=None): # auth is required even if it's None
    user_id = session.get("user.id")
    chat_id = session.get("conversation.id")
    username = session.get("user.name")
    if user_id is None:
        return
    print(Colors.BLUE+f"{user_id} joining conversation {chat_id}...")
    join_room(chat_id)

    messages = get_mesgs(chat_id)
    for msg in messages:
        send(msg, to=chat_id)
        print("\n", Colors.BLUE + f"Messages for {chat_id} sent to {username}.\n")
    print(Colors.BLUE + f"{user_id} joined conversation {chat_id} sucessfully!!") 

@socketio.on("disconnect")
def disconnect():
    chat_id = session.get("conversation.id")
    username = session.get("user.name")
    print(Colors.YELLOW + "Disconnecting...")
    leave_room(room=chat_id)

    time = datetime.now()
    content = {
        "name" : username,
        "message" : "has left room.",
        "time" : str(time)
    }
    send(content, to=chat_id)
    print(Colors.YELLOW + f"{username} left conversation {chat_id} successfully.")


if __name__ == "__main__":
    socketio.run(app, debug=True)