def module(module_name: str):
    """
    Marks a command as belonging to a specific module.
    Example: @module("core") or @module("moderation")
    """
    def wrapper(func):
        setattr(func, "__module_name__", module_name)
        return func
    return wrapper