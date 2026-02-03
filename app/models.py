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
           id TEXT UNIQUE PRIMARY KEY,
           members_id,
           created_at TEXT NOT NULL DEFAULT (datetime('now')),
           
           FOREIGN KEY (members_id) REFERENCES users(id) ON DELETE CASCADE
           );""")

cu.execute("""CREATE TABLE IF NOT EXISTS messages(
           id TEXT UNIQUE PRIMARY KEY,
           conversation_id,
           sender_id,
           content TEXT NOT NULL,
           created_at TEXT NOT NULL DEFAULT (datetime('now')),
           
           FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
           FOREIGN KEY (conversation_id) REFERENCES conversations
           );""")

cx.commit()
cu.close()
cx.close()
