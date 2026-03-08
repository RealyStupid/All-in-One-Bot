from typing import Callable, Optional
from .registry import register_command_def, register_subcommand_def


def module(name: str):
    """Attach module metadata to a callback."""
    def wrapper(func: Callable):
        setattr(func, "__module_name__", name)
        return func
    return wrapper


def command(name: str, description: str):
    """
    Decorator for standalone commands (not inside groups).
    Registers a CommandDef in the registry.
    """
    def decorator(func: Callable):
        module_name = getattr(func, "__module_name__", None)

        register_command_def(
            name=name,
            description=description,
            callback=func,
            module=module_name
        )

        return func
    return decorator


def subcommand(name: str, description: str):
    """
    Decorator used by group.command() to register subcommands.
    """
    def decorator(func: Callable):
        # module metadata already attached by @module
        setattr(func, "__subcommand_name__", name)
        setattr(func, "__subcommand_description__", description)
        return func
    return decorator