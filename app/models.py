import sqlite3

cx = sqlite3.connect("test1.db")
cu = cx.cursor()

cu.execute("PRAGMA foreig_keys = ON;")

cu.execute("""CREATE IF NOT EXISTS TABLE users(
        id TEXT UNIQUE PRIMARY KEY,
        username TEXT UNIQUE NOT NULL, 
        password_hash TEXT NOT NULL, 
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );""")

cu.execute("""CREATE IF NOT EXISTS TABLE conversations(
           id TEXT UNIQUE PRIMARY KEY,
           created_at TEXT NOT NULL DEFAULT (datetime('now'))
           );""")

cu.execute("""CREATE IF NOT EXISTS TABLE messages(
           id TEXT UNIQUE PRIMARY KEY,
           conversation_id,
           sender_id,
           content TEXT NOT NULL,
           created_at TEXT NOT NULL DEFAULT (datetime('now'))
           );""")

cx.commit()
cu.close()
cx.close()
