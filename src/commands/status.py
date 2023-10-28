import asyncio

import discord
from sqlalchemy import select, or_

from src.client import VJNClient, VJNInteraction
from src.commands.init_message import InitOrderView
from src.data.models import Order
from src.data.utils import get_session
from src.domain.entity.OrderStatus import OrderStatus, status_to_string


async def status(interaction: VJNInteraction):
    session = get_session()

    orders = session.execute(select(Order).where(Order.user_id == str(interaction.user.id))).scalars().all()
    # keep orders all order that are not canceled or expired or retrieved
    orders = [order for order in orders if order.status != OrderStatus.CANCELED
              and order.status != OrderStatus.EXPIRED
              and order.status != OrderStatus.RETRIEVED]

    # sort orders by timestamp
    orders.sort(key=lambda order: order.timestamp)

    if not orders:
        view = InitOrderView(interaction.client)
        await interaction.response.send_message(
            "Vous n'avez aucune commande en cours. Cliquez sur le bouton pour commander", ephemeral=True, view=view)
        return

    all_current_orders = session.execute(select(Order).where(
        or_(Order.status == OrderStatus.PAYED, Order.status == OrderStatus.IN_PROGRESS))).scalars().all()

    embed = discord.Embed(title="Vos commandes en cours", color=discord.Colour.blue(),
                          description="Vous recevrez un message lorsque votre commande sera prête.")
    for order in orders:
        msg = f"**{order.category}**\n{status_to_string(order.status)}"
        if order.status == OrderStatus.PAYED:
            # count the number of orders that are payed or in progress and that have been ordered before the current order
            nb_orders = len([o for o in all_current_orders if o.id != order.id and o.timestamp < order.timestamp])
            msg += f"\nPosition dans la file: {nb_orders}"
        embed.add_field(name=f"Commande #{order.pretty_id}", value=msg, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)
