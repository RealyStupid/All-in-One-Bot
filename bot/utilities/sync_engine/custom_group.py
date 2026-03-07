from typing import List, Callable
from discord import app_commands

REGISTERED_GROUPS: List[app_commands.Group] = []

def create_group(name: str, description: str) -> app_commands.Group:
    group = app_commands.Group(name=name, description=description)
    REGISTERED_GROUPS.append(group)

    def command_decorator(*d_args, **d_kwargs):
        def wrapper(func: Callable):

            cmd = app_commands.Command(
                name=d_kwargs.get("name", func.__name__),
                description=d_kwargs.get("description", func.__doc__ or "No description"),
                callback=func
            )

            group.add_command(cmd)
            return func
        return wrapper

    group.command = command_decorator
    return group