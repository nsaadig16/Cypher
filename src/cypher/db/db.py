from aiosqlite import Connection

async def create_table(conn : Connection):
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            nametag TEXT NOT NULL
        )
        """
    )
    await conn.commit()

async def insert_nametag(conn : Connection, id : int, nametag : str):
    await conn.execute(
        "INSERT OR REPLACE INTO users (id, nametag) VALUES (?,?)", (id, nametag)
    )
    await conn.commit()

async def get_nametag_from_id(conn: Connection, id : int):
    async with conn.execute("SELECT nametag FROM users WHERE id = ?", (id,)) as c:
        row = await c.fetchone()
        return row[0] if row else None

async def remove_nametag(conn: Connection, id: int):
    async with conn.execute("DELETE FROM users WHERE id = ?", (id,)) as c:
        if c.rowcount == 0:
            return False
    await conn.commit()
    return True
    