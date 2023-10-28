import discord
from discord import Interaction

from src.client import VJNInteraction, VJNClient
from src.commands.order.OrderTypeButton import OrderTypeButton
from src.domain.entity.Config import Config


async def order(interaction: VJNInteraction):
    await init_order(interaction, interaction.client)


async def init_order(interaction: Interaction, client: VJNClient):
    embed = discord.Embed(title="Order", description="Order a meal", color=discord.Color.green())
    embed.description = "Que souhaitez vous commander ?"
    view = discord.ui.View()

    config: Config = client.config

    if not config.settings.stand_open:
        await interaction.response.send_message("Le stand est fermé pour le moment.", ephemeral=True)
        return

    for cat in config.categories:
        view.add_item(OrderTypeButton(category=cat))
        field_name = f"{cat.name}{' ' + cat.emote if cat.emote is not None else ''}"
        field_value = ("À partir de: " if cat.toppings else "Prix: ") + f"{cat.price}€"
        embed.add_field(name=field_name, value=field_value, inline=False)

    try:
        await interaction.user.send(embed=embed, view=view)
    except discord.Forbidden:
        await interaction.response.send_message(
            "Impossible de vous envoyer un message privé ! Vérifiez vos paramètres de confidentialité.", ephemeral=True)
        return

    # check if interaction comes from a private message
    if interaction.channel is None:
        await interaction.response.send_message("Que souhaitez vous commander ?")
    else:
        await interaction.response.send_message("Regardez vos messages privés !", ephemeral=True)
