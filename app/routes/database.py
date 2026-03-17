# I'll put all database queries in here
import sqlite3

def getconn(): # get connection to db
    return sqlite3.connect("test1.db") # 
""" Turns out cx.execute and cu.execute are pretty much the same thing, apart from the fact that cu allows for more complex queries involving fetchone-many-all, that cx just can't handle"""

def fetch_user_by_name(username:str):
    with getconn() as cx:
        cu = cx.cursor()    # add a try and except clause here
        cu.execute("SELECT id, username FROM users WHERE username=(?)", (username,)) # comma requred to make tuple which is used by .execute()
        return cu.fetchone()

def fetch_user_by_id(uid:str):
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("SELECT id, username FROM users WHERE username=(?)", (uid,))
        return cu.fetchone()

def check_pass_by_name(pass_hash:str, username:str) -> tuple:
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("SELECT id, username FROM users WHERE username=(?) AND password_hash=(?)", (username, pass_hash))
        return cu.fetchone()

# returns user
def create_user(id:str, username:str, pass_hash:str):
    with getconn() as cu:
        try:
            cu.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", (id, username, pass_hash))
            cu.commit()
            return fetch_user_by_name(username)
        except Exception as e:
            print(e)
            cu.rollback()
            return

def fetch_all_users():
    with getconn() as cx:
        cu = cx.cursor()
        cu.execute("SELECT id, username FROM users")
        return cu.fetchall()

    