import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS messages(
                user_id INTEGER,
                username TEXT,
                direction TEXT,
                text TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        await db.commit()

async def log_message(user_id: int, username: str, direction: str, text: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            'INSERT INTO messages(user_id, username, direction, text) VALUES (?, ?, ?, ?)',
            (user_id, username, direction, text)
        )
        await db.commit()

async def fetch_user_history(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            'SELECT direction, text, timestamp FROM messages WHERE user_id=? ORDER BY timestamp',
            (user_id,)
        ) as cursor:
            rows = await cursor.fetchall()
    return rows