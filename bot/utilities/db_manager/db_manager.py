import os
from pickle import GLOBAL
import sys
import aiosqlite
import inspect

# global variables
DB_PATH = ""
GUILD_IDS = []

# helpers
def print_caller_info() -> str:
    return inspect.stack()[1].function + " in " + inspect.stack()[1].filename + ":" + str(inspect.stack()[1].lineno)

# This makes sure the GUILD_IDS list is always up to date with the database
async def refresh_guild_ids():
    global DB_PATH, GUILD_IDS
    print("[DB MANAGER] Refreshing guild IDs from database", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT guild_id FROM guild_data")
        rows = await cursor.fetchall()
        GUILD_IDS = [row[0] for row in rows]
    print("[DB MANAGER] Guild IDs refreshed:", GUILD_IDS)

async def init_data(*, path: str = None, new_instance: bool = False):
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
                welcome_message TEXT DEFAULT 'PLACEHOLDER WELCOME MESSAGE',
                leave_message TEXT DEFAULT 'PLACEHOLDER LEAVE MESSAGE'
            ) WITHOUT ROWID;
            """
        )
        await db.commit()

    await refresh_guild_ids()

# Setting and removing guilds
async def register_guild(guild_id: int):
    global DB_PATH
    print("[DB MANAGER] Registering guild with ID:", guild_id, f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO guild_data (guild_id) VALUES (?)", (guild_id,))
        await db.commit()
        
    await refresh_guild_ids()

async def unregister_guild(guild_id: int):
    global DB_PATH
    print("[DB MANAGER] Unregistering guild with ID:", guild_id, f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM guild_data WHERE guild_id = ?", (guild_id,))
        await db.commit()

    await refresh_guild_ids()

# Some server specific settings
async def set_prefix(guild_id: int, prefix: str):
    global DB_PATH
    print(f"[DB MANAGER] Setting prefix for guild {guild_id} to '{prefix}'", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET prefix = ? WHERE guild_id = ?", (prefix, guild_id))
        await db.commit()

async def reset_prefix(guild_id: int):
    global DB_PATH
    print(f"[DB MANAGER] Resetting prefix for guild {guild_id} to default '!'", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET prefix = '!' WHERE guild_id = ?", (guild_id,))
        await db.commit()

async def get_prefix(guild_id: int) -> str:
    global DB_PATH
    print(f"[DB MANAGER] Getting prefix for guild {guild_id}", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT prefix FROM guild_data WHERE guild_id = ?", (guild_id,))
        row = await cursor.fetchone()
        return row[0] if row else "!"

# Setting and remove welcome channels
async def set_welcome_channel(guild_id: int, channel_id: int):
    global DB_PATH
    print(f"[DB MANAGER] Setting welcome channel for guild {guild_id} to channel ID {channel_id}", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET welcome_channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
        await db.commit()

async def remove_welcome_channel(guild_id: int):
    global DB_PATH
    print(f"[DB MANAGER] Removing welcome channel for guild {guild_id}", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET welcome_channel_id = NULL WHERE guild_id = ?", (guild_id,))
        await db.commit()

async def get_welcome_channel(guild_id: int) -> int | None:
    global DB_PATH
    print(f"[DB MANAGER] Getting welcome channel for guild {guild_id}", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT welcome_channel_id FROM guild_data WHERE guild_id = ?", (guild_id,))
        row = await cursor.fetchone()
        return row[0] if row and row[0] is not None else None

# Setting welcome and leave messages
async def set_welcome_message(guild_id: int, message: str):
    global DB_PATH
    print(f"[DB MANAGER] Setting welcome message for guild {guild_id} message: {message}", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET welcome_message = ? WHERE guild_id = ?", (message, guild_id))
        await db.commit()

async def set_leave_message(guild_id: int, message: str):
    global DB_PATH
    print(f"[DB MANAGER] Setting leave message for guild {guild_id} message: {message}", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE guild_data SET leave_message = ? WHERE guild_id = ?", (message, guild_id))
        await db.commit()

async def get_welcome_message(guild_id: int) -> str | None:
    global DB_PATH
    print(f"[DB MANAGER] Getting welcome message for guild {guild_id}", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT welcome_message FROM guild_data WHERE guild_id = ?", (guild_id,))
        row = await cursor.fetchone()
        return row[0] if row and row[0] is not None else None

async def get_leave_message(guild_id: int) -> str | None:
    global DB_PATH
    print(f"[DB MANAGER] Getting leave message for guild {guild_id}", f"\nCaller info:\n", print_caller_info())
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT leave_message FROM guild_data WHERE guild_id = ?", (guild_id,))
        row = await cursor.fetchone()
        return row[0] if row and row[0] is not None else None

# Module management
# This is for storing module specific data, such as whether a module is enabled or not.
async def module_init():
    global DB_PATH

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS guild_modules (
                guild_id    INTEGER NOT NULL,
                module_name TEXT    NOT NULL,
                enabled     INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY (guild_id, module_name)
            )
        """)
        await db.commit()

# Set the enabled state of a module for a specific guild
async def set_module_enabled(guild_id: int, module_name: str, enabled: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        if enabled:
            await db.execute("""
                INSERT INTO guild_modules (guild_id, module_name, enabled)
                VALUES (?, ?, 1)
                ON CONFLICT(guild_id, module_name) DO UPDATE SET enabled = 1
            """, (guild_id, module_name))
        else:
            await db.execute("""
                UPDATE guild_modules
                SET enabled = 0
                WHERE guild_id = ? AND module_name = ?
            """, (guild_id, module_name))
        await db.commit()

# Check if a module is enabled for a specific guild
async def is_module_enabled(guild_id: int, module_name: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT enabled FROM guild_modules
            WHERE guild_id = ? AND module_name = ?
        """, (guild_id, module_name))
        row = await cursor.fetchone()
        return bool(row and row[0])

# Retrieve a list of enabled modules for a specific guild
async def get_enabled_modules_for_guild(guild_id: int) -> list[str]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT module_name FROM guild_modules
            WHERE guild_id = ? AND enabled = 1
        """, (guild_id,))
        rows = await cursor.fetchall()
        return [r[0] for r in rows]

async def remove_all_modules_for_guild(guild_id: int):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            "DELETE FROM guild_modules WHERE guild_id = ?",
            (guild_id,)
        )
        await db.commit()