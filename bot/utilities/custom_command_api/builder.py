from discord import app_commands
from .definitions import CommandDef, GroupDef
import functools

def build_command(defn: CommandDef) -> app_commands.Command:
    original_callback = defn.callback

    # ---------------------------------------------------------
    # PERMISSION WRAPPING
    # ---------------------------------------------------------
    if hasattr(original_callback, "__permission_check__"):
        permission_check = original_callback.__permission_check__

        @functools.wraps(original_callback)
        async def wrapped(*args, **kwargs):
            interaction = args[0]  # always the first arg

            allowed = await permission_check(interaction)
            if not allowed:
                # If the interaction has not been responded to yet:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "❌ You do not have permission to use this command.",
                        ephemeral=True
                    )
                else:
                    # If something already responded (rare), use followup
                    await interaction.followup.send(
                        "❌ You do not have permission to use this command.",
                        ephemeral=True
                    )
                return

            return await original_callback(*args, **kwargs)

        callback = wrapped
    else:
        callback = original_callback

    # ---------------------------------------------------------
    # BUILD THE COMMAND
    # ---------------------------------------------------------
    cmd = app_commands.Command(
        name=defn.name,
        description=defn.description,
        callback=callback
    )

    # ---------------------------------------------------------
    # AUTOCOMPLETE SUPPORT
    # ---------------------------------------------------------
    if hasattr(defn.callback, "__autocomplete__"):
        for param_name, handler in defn.callback.__autocomplete__.items():
            if param_name in cmd.parameters:
                cmd.parameters[param_name].autocomplete = True
            cmd.autocomplete(param_name)(handler)

    return cmd


def build_group(defn: GroupDef) -> app_commands.Group:
    group = app_commands.Group(
        name=defn.name,
        description=defn.description
    )

    for sub in defn.subcommands:
        cmd = build_command(sub)
        group.add_command(cmd)

    return group