
import asyncio

import discord

from src.client import VJNClient
from src.client import VJNClient, VJNInteraction
from src.domain.entity.guildConfig import Config
from src.orders.order.OrderButton import OrderTypeButton


async def order(interaction: VJNInteraction):
    embed =  discord.Embed(title="Order", description="Order a meal", color=discord.Color.green())
    view = discord.ui.View()

    config : Config = interaction.client.config
    for cat in config.categories:
        button = OrderTypeButton(category=cat)
        view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


