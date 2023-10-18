import discord
from discord import Interaction

from src.commands.order import order2


class InitOrderView(discord.ui.View):

    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(label="Commander", style=discord.ButtonStyle.green, custom_id="start_order", emoji="🍔")
    async def start_order(self, interaction: Interaction, button: discord.ui.Button):
        await order2(interaction, self.client)


async def init_message(interaction: Interaction):
    """
    Initialize the message to order a meal (staff only)
    @param interaction: Interaction
    """

    view = InitOrderView(interaction.client)
    embed = discord.Embed(title="Commande", description="Commandez un repas", color=discord.Color.green())
    embed.add_field(name="Catégories",
                    value="\n".join([category.name for category in interaction.client.config.categories]))
    await interaction.response.send_message("Done", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)
