from typing import Callable, Optional, List


class CommandDef:
    def __init__(self, name: str, description: str,
                 callback: Callable, module: Optional[str]):
        self.name = name
        self.description = description
        self.callback = callback
        self.module = module


class GroupDef:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.subcommands: List[CommandDef] = []

    def add_subcommand(self, cmd: CommandDef):
        self.subcommands.append(cmd)