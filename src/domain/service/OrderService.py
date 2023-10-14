import aiohttp
import discord
from discord import Colour

from src.client import VJNClient
from src.commands.order.OrderStatusChange import ChangeStatusButton
from src.data.models import Order
from src.domain.entity.Config import Config
from src.domain.entity.OrderStatus import OrderStatus
from src.utils import setup_logging

_log = setup_logging(__name__)


async def new_order(client: VJNClient, order: Order):
    embed = discord.Embed(title=f"Nouvelle commande #{order.pretty_id}", color=Colour.blue())
    embed.add_field(name="Catégorie", value=order.category, inline=False)
    if order.toppings:
        embed.add_field(name="Toppings", value="\n".join([topping.name for topping in order.toppings]), inline=False)
    embed.add_field(name="Prix", value=f"{order.total_cost}€" if order.total_cost > 0 else "Gratuit", inline=False)
    embed.set_footer(text=f"Commande #{order.pretty_id} ({order.id})")

    try:
        user = await client.fetch_user(int(order.user_id))
        embed.add_field(name="Utilisateur", value=f"{user.mention} ({user.name}#{user.discriminator})", inline=False)
    except discord.NotFound:
        embed.add_field(name="Utilisateur", value=f"User: {order.user_id}", inline=False)

    view = discord.ui.View()
    view.add_item(ChangeStatusButton(order.id, OrderStatus.PAYED if order.total_cost > 0 else OrderStatus.IN_PROGRESS))

    channel = client.get_channel(client.config.settings.channel)

    if channel is None:
        _log.error("Could not find channel with ID %d", client.config.settings.channel)
        return

    await channel.send(embed=embed, view=view)


