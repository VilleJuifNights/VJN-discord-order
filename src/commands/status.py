import asyncio

import discord
from sqlalchemy import select

from src.client import VJNClient, VJNInteraction
from src.data.models import Order
from src.data.utils import get_session
from src.domain.entity.OrderStatus import OrderStatus, status_to_string


async def status(interaction: VJNInteraction):
    session = get_session()

    orders = session.execute(select(Order).where(Order.user_id == str(interaction.user.id))).scalars().all()
    print(orders)
    # keep orders all order that are not canceled or expired or retrieved
    orders = [order for order in orders if order.status != OrderStatus.CANCELED
              and order.status != OrderStatus.EXPIRED
              and order.status != OrderStatus.RETRIEVED]

    if not orders:
        await interaction.response.send_message(
            "Vous n'avez aucune commande en cours. Utilisez /order pour en créer une.", ephemeral=True)
        return
    embed = discord.Embed(title="Vos commandes en cours", color=discord.Colour.blue(),
                          description="Vous recevrez un message lorsque votre commande sera prête.")
    for order in orders:
        embed.add_field(name=f"Commande #{order.pretty_id}",
                        value=f"**Catégorie:** {order.category}\n**Status:** {status_to_string(order.status)}",
                        inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)
