import discord

from src.client import VJNInteraction
from src.commands.order import OrderTypeButton
from src.domain.entity.Config import Config


async def create(interaction: VJNInteraction, login: str):
    embed = discord.Embed(title="Order", description="Order a meal", color=discord.Color.green())
    embed.description = "Sélectionnez la catégorie de la commande"
    embed.add_field(name="Login", value=login, inline=False)
    view = discord.ui.View()

    config: Config = interaction.client.config
    for cat in config.categories:
        view.add_item(OrderTypeButton(category=cat, login=login))
        field_name = f"{cat.name}{' ' + cat.emote if cat.emote is not None else ''}"
        field_value = ("À partir de: " if cat.toppings else "Prix: ") + f"{cat.price}€"
        embed.add_field(name=field_name, value=field_value, inline=False)

    await interaction.user.send(embed=embed, view=view)
    await interaction.response.send_message("Commande pour `"+login+"`", ephemeral=True)
