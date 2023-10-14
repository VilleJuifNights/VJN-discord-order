import discord

from src.client import VJNInteraction
from src.commands.order.OrderTypeButton import OrderTypeButton
from src.domain.entity.Config import Config


async def order(interaction: VJNInteraction):
    embed = discord.Embed(title="Order", description="Order a meal", color=discord.Color.green())
    embed.description = "Que souhaitez vous commander ?"
    view = discord.ui.View()

    config: Config = interaction.client.config
    for cat in config.categories:
        view.add_item(OrderTypeButton(category=cat))
        field_name = f"{cat.name}{' ' + cat.emote if cat.emote is not None else ''}"
        field_value = ("À partir de: " if cat.toppings else "Prix: ") + f"{cat.price}€"
        embed.add_field(name=field_name,value=field_value, inline=False)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
