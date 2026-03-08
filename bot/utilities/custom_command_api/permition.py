def owner_only(allow_guild_owner: bool = False, allow: list[int] = None):
    allow = allow or []

    def decorator(func):
        async def check(interaction):
            bot_owner_id = interaction.client.owner_id
            user_id = interaction.user.id

            # Bot owner
            if user_id == bot_owner_id:
                return True

            # Guild owner
            if allow_guild_owner and interaction.guild is not None:
                if user_id == interaction.guild.owner_id:
                    return True

            # Custom allowed list
            if user_id in allow:
                return True

            return False

        func.__permission_check__ = check
        return func

    return decorator