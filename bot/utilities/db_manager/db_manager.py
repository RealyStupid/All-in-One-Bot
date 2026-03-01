import os
import sys
import aiosqlite

# global variables
DB_PATH = ""

async def init_data(path: str = None, new_instance: bool = False):
    print("[DB MANAGER] Initializing database manager with path:", path, "and new_instance:", new_instance)
    if path is None:
        print("[DB MANAGER] No path provided, pease set a path before running the bot.")
        sys.exit(1)

    if new_instance:
        os.remove(path) if os.path.exists(path) else None

    global DB_PATH
    DB_PATH = path

    await guild_data_init()
    print("[DB MANAGER] Database manager initialized successfully with path:", DB_PATH)

# Guild data management
# This handles creating the .db file and the guild_data table,
# as well as inserting new guilds when the bot joins a server and removing them when it leaves. 
# It also includes functions change data and add new guilds.
async def guild_data_init():
    global DB_PATH

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS guild_data (
                guild_id INTEGER PRIMARY KEY,
                prefix TEXT DEFAULT '!',
                welcome_channel_id INTEGER,
                welcome_message TEXT,
                leave_message TEXT
            ) WITHOUT ROWID;
            """
        )
        await db.commit()

# Setting and removing guilds
async def register_guild(guild_id: int):
    global DB_PATH
    print("[DB MANAGER] Registering guild with ID:", guild_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO guild_data (guild_id) VALUES (?)", (guild_id,))
        await db.commit()

async def unregister_guild(guild_id: int):
    global DB_PATH
    print("[DB MANAGER] Unregistering guild with ID:", guild_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM guild_data WHERE guild_id = ?", (guild_id,))
        await db.commit()

async def get_guild_ids() -> list[int]:
    global DB_PATH
    print("[DB MANAGER] Guild ids were requested")
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT guild_id FROM guild_data")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]

# Some server specific settings
async def set_prefix(guild_id: int, prefix: str):
    global DB_PATH
    print(f"[DB MANAGER] Setting prefix for guild {guild_id} to '{prefix}'")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET prefix = ? WHERE guild_id = ?", (prefix, guild_id))
        await db.commit()

async def reset_prefix(guild_id: int):
    global DB_PATH
    print(f"[DB MANAGER] Resetting prefix for guild {guild_id} to default '!'")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET prefix = '!' WHERE guild_id = ?", (guild_id,))
        await db.commit()

async def get_prefix(guild_id: int) -> str:
    global DB_PATH
    print(f"[DB MANAGER] Getting prefix for guild {guild_id}")
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT prefix FROM guild_data WHERE guild_id = ?", (guild_id,))
        row = await cursor.fetchone()
        return row[0] if row else "!"

# Setting and remove welcome channels
async def set_welcome_channel(guild_id: int, channel_id: int):
    global DB_PATH
    print(f"[DB MANAGER] Setting welcome channel for guild {guild_id} to channel ID {channel_id}")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET welcome_channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
        await db.commit()

async def remove_welcome_channel(guild_id: int):
    global DB_PATH
    print(f"[DB MANAGER] Removing welcome channel for guild {guild_id}")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET welcome_channel_id = NULL WHERE guild_id = ?", (guild_id,))
        await db.commit()

async def get_welcome_channel(guild_id: int) -> int | None:
    global DB_PATH
    print(f"[DB MANAGER] Getting welcome channel for guild {guild_id}")
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT welcome_channel_id FROM guild_data WHERE guild_id = ?", (guild_id,))
        row = await cursor.fetchone()
        return row[0] if row and row[0] is not None else None

# Setting welcome and leave messages
async def set_welcome_message(guild_id: int, message: str):
    global DB_PATH
    print(f"[DB MANAGER] Setting welcome message for guild {guild_id} message: {message}")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET welcome_message = ? WHERE guild_id = ?", (message, guild_id))
        await db.commit()

async def set_leave_message(guild_id: int, message: str):
    global DB_PATH
    print(f"[DB MANAGER] Setting leave message for guild {guild_id} message: {message}")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET leave_message = ? WHERE guild_id = ?", (message, guild_id))
        await db.commit()

async def get_welcome_message(guild_id: int) -> str | None:
    global DB_PATH
    print(f"[DB MANAGER] Getting welcome message for guild {guild_id}")
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT welcome_message FROM guild_data WHERE guild_id = ?", (guild_id,))
        row = await cursor.fetchone()
        return row[0] if row and row[0] is not None else None