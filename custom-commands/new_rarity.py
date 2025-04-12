# Improved rarity command originally created by Nixter and converted from CarFigures to Ballsdex by me.


    @app_commands.command()
    @app_commands.checks.cooldown(1, 60, key=lambda i: i.user.id)
    async def rarity(
        self,
        interaction: discord.Interaction,
        reverse: bool = False,
    ):
        """
        Show the rarity list of the bot

        Parameters
        ----------
        reverse: bool
            Whether to show the rarity list in reverse
        """

        # Filter enabled collectibles
        enabled_collectibles = [x for x in balls.values() if x.enabled]

        if not enabled_collectibles:
            await interaction.response.send_message(
                f"There are no collectibles registered in {settings.bot_name} yet.",
                ephemeral=True,
            )
            return

        # Group collectibles by rarity
        rarity_to_collectibles = {}
        for collectible in enabled_collectibles:
            rarity = collectible.rarity
            if rarity not in rarity_to_collectibles:
                rarity_to_collectibles[rarity] = []
            rarity_to_collectibles[rarity].append(collectible)

        # Sort the rarity_to_collectibles dictionary by rarity
        sorted_rarities = sorted(rarity_to_collectibles.keys(), reverse=reverse)

        # Display collectibles grouped by rarity
        entries = []
        for rarity in sorted_rarities:
            collectible_names = "\n".join(
                [
                    f"\u200b ⋄ {self.bot.get_emoji(c.emoji_id) or 'N/A'} {c.country}"
                    for c in rarity_to_collectibles[rarity]
                ]
            )
            entry = (f"∥ Rarity: {rarity}", f"{collectible_names}")
            entries.append(entry)

        # Starting the Pager
        source = FieldPageSource(entries, per_page=7, inline=False, clear_description=False)
        source.embed.title = f"{settings.bot_name} Rarity List"
        source.embed.colour = discord.Colour.blurple()
        pages = Pages(source=source, interaction=interaction, compact=False)
        await pages.start()
