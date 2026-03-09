<h1 align="center">---{THE ALL IN ONE BOT}---</h1>

## This is a bot made by [RealyStupid](https://github.com/RealyStupid).
The goal of **All In One Bot** is simple:  
**Create one bot that can do everything — cleanly, modularly, and without the chaos that usually comes with large Discord bots.**

This project is the spiritual successor to the original  
[Everything Bot](https://github.com/RealyStupid/Everything-Bot),  
but rebuilt from the ground up with a **new, more stable, more scalable architecture**.

---

## Why this bot exists
Most Discord bots fall into one of two categories:

1. **Small bots** with a handful of commands  
2. **Massive bots** that become impossible to maintain

All In One Bot aims to be the best of both worlds:

- A single bot that can contain *every* feature  
- But organized into **modules** that can be enabled or disabled  
- With commands that appear or disappear dynamically  
- Without needing to restart the bot  
- Without cluttering the UI  
- Without breaking Discord’s slash command system

This is only possible because of the **custom command API** and the **Sync Engine**.

---

<h2 align="center">---{THE NEW CUSTOM COMMAND API}---</h2>

All In One Bot does **not** use Discord.py’s built‑in slash command decorators.

Instead, it uses a **custom command definition system** designed specifically for:

- Large bots  
- Modular architectures  
- Dynamic command loading  
- Per‑guild customization  
- Global command support  
- Autocomplete  
- Hot‑reloading  
- Avoiding decorator conflicts  
- Avoiding Discord’s “command already registered” errors  
- Avoiding the nightmare of manually syncing commands

### Why a new API was needed
Discord.py’s built‑in slash command system is great for small bots, but it breaks down when:

- You have hundreds of commands  
- Commands need to be enabled/disabled per guild  
- Commands need to be hidden dynamically  
- Commands belong to modules  
- Commands need to be rebuilt on the fly  
- You want to avoid sync conflicts  
- You want to avoid duplicate command registration  
- You want a clean separation between:
  - **definition**
  - **execution**
  - **syncing**

The custom API solves all of these problems.

### What the new API provides
- A clean `Group` system for slash command groups  
- A `@module()` decorator to assign commands to modules  
- A registry that stores all commands before they are built  
- A builder that converts definitions → Discord commands  
- An execution manager that registers commands into Discord.py  
- A sync engine that pushes commands to Discord  
- Full support for:
  - global commands  
  - guild commands  
  - autocomplete  
  - subcommands  
  - dynamic module filtering  

This architecture is designed for **scalability**, **maintainability**, and **future expansion**.

---

<h2 align="center">---{LICENSE}---</h2>

this project is free for anyone to review and edit. But you cannot host this for your own bot or gain.

---

## The bot is currently in development.
This repository exists to show progress and gather feedback.  
The bot is not yet ready for public use.

---

<h2 align="center">---{FEATURES}---</h2>

All In One Bot uses:

- **Discord global slash commands**
- **Guild‑specific slash commands**
- **A custom Sync Engine**
- **A custom Command API**
- **A module system that controls which commands appear**

### Why modules matter
Modules allow commands to be:

- Enabled  
- Disabled  
- Hidden  
- Shown  
- Synced  
- Desynced  

…all without restarting the bot.

This makes the bot **fully customizable per server**.

### Where this version deviates from Everything Bot
This Sync Engine is:

- More stable  
- More expandable  
- More predictable  
- Easier to maintain  
- Designed for large‑scale bots  
- Designed to avoid Discord’s sync conflicts  
- Designed to allow commands to be added like normal Python functions  

---

## Global Commands

### **Module Commands**
- `/module enable <module>` — enables a module and its commands  
- `/module disable <module>` — disables a module and its commands  
- `/module list` — lists all modules  
- `/module enabled` — lists enabled modules  

### **Customization Commands**
- `/customization prefix <prefix>` — changes the bot’s prefix  
- `/customization nickname <nickname>` — changes the bot’s nickname  

---

<h2 align="center">---{CONTRIBUTIONS}---</h2>

As explained under License, contributions are allowed only with explicit permission.

Reading and giving feedback is allowed for everyone.

To gain permission, contact: **therealrealystupid** on Discord.

Information needed before permission is granted:
- Your GitHub profile  
- Your most notable repo  
- Your skills  
- What you want to contribute  
- How long you plan to stay a contributor  
