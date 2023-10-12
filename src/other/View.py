import discord


class ReopenView(discord.ui.View):
    def __init__(self):
        """
        Init the view
        """
        super().__init__()
        self.timeout = 8 * 60 * 60  # 8 hours before the view times out

    # @discord.ui.button(label="Reopen", style=discord.ButtonStyle.green, emoji="🔓")
    # async def reopen(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await tickets.reopen_ticket(interaction)
