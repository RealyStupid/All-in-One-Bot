from .registry import register_standalone_command_def

class slash:
    @staticmethod
    def command(name: str, description: str):
        def wrapper(func):
            module_name = getattr(func, "__module_name__", None)

            register_standalone_command_def(
                name=name,
                description=description,
                callback=func,
                module=module_name
            )

            return func
        return wrapper