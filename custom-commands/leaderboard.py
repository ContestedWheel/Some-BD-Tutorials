# Leaderboard command made by wascertified

    @app_commands.command()
    async def leaderboard(self, interaction: discord.Interaction):
        """
        Show the leaderboard of users with the most caught countryballs.
        """
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        players = await Player.annotate(ball_count=Count("balls")).order_by("-ball_count").limit(10)
        
        if not players:
            await interaction.followup.send("No players found.", ephemeral=True)
            return

        entries = []
        for i, player in enumerate(players):
            user = self.bot.get_user(player.discord_id)
            if user is None:
                user = await self.bot.fetch_user(player.discord_id)

            entries.append((f"{i + 1}. {user.name}", f"Balls: {player.ball_count}"))

        source = FieldPageSource(entries, per_page=5, inline=False)
        source.embed.title = "Top 10 players"
        source.embed.color = discord.Color.gold()
        source.embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        pages = Pages(source=source, interaction=interaction)
        await pages.start(ephemeral=True)
