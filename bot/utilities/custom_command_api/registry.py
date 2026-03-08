from typing import List
from .definitions import CommandDef, GroupDef

GLOBAL_COMMAND_DEFS: List[CommandDef] = []
MODULE_COMMAND_DEFS: List[CommandDef] = []
GROUP_DEFS: List[GroupDef] = []

# Standalone slash command registries
STANDALONE_GLOBAL_COMMAND_DEFS: List[CommandDef] = []
STANDALONE_MODULE_COMMAND_DEFS: List[CommandDef] = []


def register_command_def(name, description, callback, module):
    """Register a grouped subcommand."""
    cmd = CommandDef(name, description, callback, module)

    if module is None:
        GLOBAL_COMMAND_DEFS.append(cmd)
    else:
        MODULE_COMMAND_DEFS.append(cmd)

    return cmd


def register_group_def(group: GroupDef):
    GROUP_DEFS.append(group)
    return group


def register_subcommand_def(group: GroupDef, name, description, callback, module):
    """Register a subcommand inside a group."""
    cmd = CommandDef(name, description, callback, module)
    group.add_subcommand(cmd)
    return cmd

# Standalone Slash Command Registration
def register_standalone_command_def(name, description, callback, module):
    """
    Register a standalone slash command (not inside a group).
    """
    cmd = CommandDef(name, description, callback, module)

    if module is None:
        STANDALONE_GLOBAL_COMMAND_DEFS.append(cmd)
    else:
        STANDALONE_MODULE_COMMAND_DEFS.append(cmd)

    return cmd