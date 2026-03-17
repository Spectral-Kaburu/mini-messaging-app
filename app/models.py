import sqlite3

cx = sqlite3.connect("test1.db")
cu = cx.cursor()

cu.execute("PRAGMA foreign_keys = ON;")

cu.execute("""CREATE TABLE IF NOT EXISTS users(
        id TEXT UNIQUE PRIMARY KEY,
        username TEXT UNIQUE NOT NULL, 
        password_hash TEXT NOT NULL, 
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );""")


# Figure out how to name these conversations, such that this is the only table queried in the dashboard
# I'm assuming a play on the members_id, maybe add a members_name
cu.execute("""CREATE TABLE IF NOT EXISTS conversations(
           id TEXT NOT NULL,
           name TEXT NOT NULL,
           user_id,
           created_at TEXT NOT NULL DEFAULT (datetime('now')),
           FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
           );""")

cu.execute("""CREATE TABLE IF NOT EXISTS messages(
           id TEXT UNIQUE PRIMARY KEY,
           content TEXT NOT NULL,
           chat_id,
           sender_id,
           created_at TEXT NOT NULL DEFAULT (datetime('now')),
           FOREIGN KEY (chat_id) REFERENCES conversations(id) ON DELETE CASCADE,
           FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
           );""")

cx.commit()
cu.close()
cx.close()
