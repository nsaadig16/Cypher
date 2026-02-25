from sqlite3 import Connection, Cursor

def create_table(conn : Connection, c : Cursor):
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            nametag TEXT NOT NULL
        )
        """
    )
    conn.commit()

def insert_nametag(conn : Connection, c: Cursor, id : int, nametag : str):
    c.execute(
        "INSERT OR REPLACE INTO users (id, nametag) VALUES (?,?)", (id, nametag)
    )
    conn.commit()

def get_nametag_from_id(conn : Connection, c : Cursor, id : int):
    c.execute("SELECT nametag FROM users WHERE id = ?", (id,))
    row = c.fetchone()
    return row        

def remove_nametag(conn: Connection, c : Cursor, id : int):
    c.execute("DELETE FROM users WHERE id = ?", (id,))
    if c.rowcount == 0:
        return False
    else:
        conn.commit()
        return True
    