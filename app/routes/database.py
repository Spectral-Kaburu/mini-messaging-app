# I'll put all database queries in here
from ..helpers.general import Colors
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
DB = os.getenv("DB")

print(Colors.BLUE+"Database in use: "+Colors.GREEN+f"{DB}.")

def getconn(): # get connection to db
    return sqlite3.connect(DB) # 
""" Turns out cx.execute and cu.execute are pretty much the same thing, apart from the fact that cu allows for more complex queries involving fetchone-many-all, that cx just can't handle"""

## AUTH
def fetch_user_by_name(username:str) -> tuple:
    with getconn() as cx:
        cu = cx.cursor()    # add a try and except clause here
        cu.execute("SELECT id, username, password_hash FROM users WHERE username=(?)", (username,)) # comma requred to make tuple which is used by .execute()
        return cu.fetchone()

def fetch_user_by_id(uid:str) -> tuple:
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("SELECT id, username FROM users WHERE username=(?)", (uid,))
        return cu.fetchone()

# returns user
def create_user(id:str, username:str, pass_hash:bytes) -> tuple:
    with getconn() as cu:
        try:
            cu.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", (id, username, pass_hash))
            cu.commit()
            return fetch_user_by_name(username)
        except Exception as e:
            print(e)
            cu.rollback()
            return

def fetch_all_users() -> list:
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("SELECT id, username FROM users")
        return cu.fetchall()

## DASHBOARD
def get_chats(user_id:str) -> list:
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("SELECT id, name FROM conversations WHERE user_id=(?)", (user_id,))
        return cu.fetchall()

## CONVERSATIONS
def fetch_one_mesg(mesg_id, chat_id):
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("SELECT * FROM messages WHERE id=(?) AND chat_id=(?)", (mesg_id, chat_id))
        return cu.fetchone()

def get_mesgs(chat_id:str) -> list:
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("SELECT * FROM messages WHERE chat_id=(?)", (chat_id,))
        return cu.fetchall()

def send_msg(msg_id:str, chat_id:str, content:str, sender_id:str) -> tuple:
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("INSERT INTO messages(id, content, chat_id, sender_id) VALUES (?, ?, ?)", (msg_id, content, chat_id, sender_id))
        return fetch_one_mesg(msg_id, chat_id)