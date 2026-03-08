# All In One Bot: Custom Command API Documentation

A complete guide for developers working on Everything Bot’s custom slash‑command framework.

## 1. Overview

All In One Bot does not use Discord.py’s built‑in slash command decorators.
Instead, it uses a custom command definition system that:
- Stores command definitions in a registry
- Builds Discord commands dynamically
- Syncs commands per‑guild based on enabled modules
- Supports global commands
- Supports groups and subcommands
- Supports autocomplete
- Avoids decorator conflicts
- Allows hot‑reloading and modularity

This system is composed of:

| Component | Perpose |
|-----------|---------|
| Groups | Defines a slash command group (e.g, `/module`)
| `@module()` | Assigns a module or marks a command as global
| Registry | Stores all commands & group definitions
| Builder | Converts definitions -> Discord app commands
| Sync Engine | Syncs commands to Discord (guild or global)

---
## 2. Command Definition Basics
Slash commands are defined at module level, not inside Cogs.
Example:
```Python
from utilities.custom_command_api import Group, module

my_group = Group("example", "Example commands")

@my_group.command("ping", "Ping the bot")
@module("fun")
async def ping(interaction):
    await interaction.response.send_message("Pong!")
```

Key Rules:
- Commands must not be inside a Cog class
- Commands must not use Discord.py decorators
- Commands must be defined at module level
- Commands must use `@module()` to specify their module
- Groups are not Discord objects, they are definitions
---
## 3. Global Commands
A command becomes global when:
```
@module(None)
```

Example:
```Python
@my_group.command("info", "Show bot info")
@module(None)
async def info(interaction):
```
Global commands:
- Are synced globally
- Are not filtered by module enable/disable
- Always appear in every guild
- Must be registered by the execution manager at startup
---
## 4. Groups
Groups are created like this:
```Python
settings = Group("settings", "bot setting")
```
Groups:
- Are NOT Discord objects
- Are stored in the registry
- Are built dynamically by the sync engine
- Can contain multiple subcommands

Example:
```Python
@settings.command("prefix", "Set prefix")
@module(None)
async def set_prefix(interaction, prefix: str):
    ...
```
---
## 5. Modules
Modules allow commands to be enabled/disabled per guild.

A command belongs to a module:
```Python
@module("module")
```
A command is global:
```Python
@module("None")
```
Module names must match a module type inside `module_enum.py`:
```Python
from enum import Enum

class ModuleEnum(Enum):
    TEST_ENUM = "test"
    MODERATION = "moderation"
    MODULE = "module"

    @classmethod
    def list(cls):
        return [m.value for m in cls]
```
---
## 6. Autocomplete
Autocomplete is attached by setting:
```Python
command.__autocomplete__ = {
    "argument_name": autocomplete_function
}
```

Example:
```Python
async def auto_modules(interaction, current):
    return [...]

@settings.command("enable", "Enable a module")
@module(None)
async def enable_module(interaction, module_name: str):
    ...

enable_module.__autocomplete__ = {
    "module_name": auto_modules
}
```
---
## 7. Registry Structure
The registry stores:
- GLOBAL_COMMAND_DEFS
- MODULE_COMMAND_DEFS
- GROUP_DEFS

- Each definition contains:
- name
- description
- callback
- module
- autocomplete
- parameters
This allows the sync engine to rebuild commands dynamically.
---
## 8. Builder System
The builder converts definitions -> Discord commands.

`build_command(defn)`

Creates a Discord app_commands.Command.

`build_group(defn)`

Creates a Discord app_commands.Group.

The builder attaches:
- Name
- Description
- Callback
- Autocomplete
- Parameters
---
## 9. Execution Manager (Critical Component)
The execution manager registers commands into Discord.py’s execution router.
Without this, commands sync but do not execute.

File: `utilities/sync_engine/execution_manager.py`

Responsibilities:
- Build global commands from the registry
- Register them into bot.tree
- Ensure Discord.py can route interactions
- Does not sync — only registers
Called in main.py after cogs load.
---
## 10. Sync Engine
The sync engine handles:

Per‑guild sync
sync_guild(bot, guild_id)
- Clears guild commands
- Builds commands based on enabled modules
- Adds them to the tree
- Syncs them

Global sync
sync_global(bot)
- Clears global commands
- Builds global commands
- Adds them to the tree
- Syncs them

Execution manager must run BEFORE syncing
Otherwise commands exist on Discord but cannot execute.

---
## 11. Debugging Guide

Command not found?
- Execution manager not run
- Registry empty at startup
- Global commands not registered
- Sync not run after changes

- Autocomplete not working?
- Missing `__autocomplete__`
- Parameter name mismatch
- Sync not run

- Group not appearing?
- No allowed subcommands
- Module disabled
- Registry not populated
---
## 12. Full Command Lifecycle
Here’s how a command travels through the system:
### 1. Definition Layer
Developer writes:
```Python
@group.command(...)
@module(...)
async def callback(...):
```

### 2. Registry Layer
The decorator stores the definition in:
- GLOBAL_COMMAND_DEFS
- MODULE_COMMAND_DEFS
- GROUP_DEFS

### 3. Execution Layer
At startup:
```Python
await register_global_commands(bot)
```

### 4. Sync Layer
Developer runs:
```
!sync global
```
or
```
!sync guild
```
to push it to discord.

### 5. Execution
User runs /(command synced)

Discord sends interaction -> Discord.py -> your callback.

---
## 13. Creating a New Command (Full Example)
```Python
from utilities.custom_command_api import Group, module
import discord

admin = Group("admin", "Admin tools")

@admin.command("announce", "Send an announcement")
@module("moderation")
async def announce(interaction, message: str):
    await interaction.response.send_message(f"Announcement: {message}")
```
---
## 14. Creating a New Group
```Python
fun = Group("fun", "Fun commands")

@fun.command("roll", "Roll a dice")
@module("fun")
async def roll(interaction, sides: int = 6):
    import random
    await interaction.response.send_message(f"You rolled {random.randint(1, sides)}!")
```
