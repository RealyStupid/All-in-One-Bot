from .definitions import GroupDef
from .registry import register_group_def, register_subcommand_def


class Group:
    def __init__(self, name: str, description: str):
        self.defn = GroupDef(name, description)
        register_group_def(self.defn)

    def command(self, name: str, description: str):
        def decorator(func):
            module_name = getattr(func, "__module_name__", None)

            register_subcommand_def(
                group=self.defn,
                name=name,
                description=description,
                callback=func,
                module=module_name
            )

            return func
        return decorator