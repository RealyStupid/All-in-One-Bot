def autocomplete(**mapping):
    """
    Usage:
        @autocomplete(param=handler)
    Works exactly like discord.app_commands.autocomplete.
    """
    def decorator(func):
        # Create metadata storage if missing
        if not hasattr(func, "__autocomplete__"):
            func.__autocomplete__ = {}

        # Add each param->handler mapping
        for param, handler in mapping.items():
            func.__autocomplete__[param] = handler

        return func

    return decorator