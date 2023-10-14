import uuid

import discord
from discord import ButtonStyle
from sqlalchemy import select

from src.client import VJNInteraction
from src.data.models import Order
from src.data.utils import get_session
from src.domain.entity.OrderStatus import OrderStatus, status_to_button_label, next_status


class ChangeStatusButton(discord.ui.Button):

    def __init__(self, order_id: uuid.UUID, status: OrderStatus):
        super().__init__(label=status_to_button_label(status), custom_id=f"order_{order_id}_{status.name}",
                         style=ButtonStyle.green)
        self.order = order_id
        self.status = status

    async def callback(self, interaction: VJNInteraction):
        await interaction.response.defer(ephemeral=True)
        session = get_session()

        order = session.execute(select(Order).where(Order.id == self.order)).scalar_one_or_none()
        if order is None:
            raise Exception(f"Order with id {self.order} not found")
        order.status = self.status

        session.commit()

        if self.status == OrderStatus.RETRIEVED:
            # delete message
            await interaction.message.delete()
            return

        # get embed from message interaction
        embed = interaction.message.embeds[0]
        view = discord.ui.View()
        view.add_item(ChangeStatusButton(self.order, next_status(self.status)))

        await interaction.message.edit(embed=embed, view=view)

        if self.status == OrderStatus.IN_PROGRESS:
            # send message to user
            try:
                user = await interaction.client.fetch_user(int(order.user_id))
                await user.send(
                    f"Votre commande #{order.pretty_id} est en cours de préparation et sera bientôt prête !")
            except discord.NotFound or discord.Forbidden:
                await interaction.followup.send(f"Impossible de contacter l'utilisateur {order.user_id} pour lui "
                                                f"annoncer que sa commande #{order.pretty_id} est en cours de "
                                                f"préparation.")

        if self.status == OrderStatus.COMPLETED:
            # send message to user
            try:
                user = await interaction.client.fetch_user(int(order.user_id))
                await user.send(f"Votre commande #{order.pretty_id} est prête !")
            except discord.NotFound or discord.Forbidden:
                await interaction.followup.send(f"Impossible de contacter l'utilisateur {order.user_id} pour lui "
                                                f"annoncer que sa commande #{order.pretty_id} est prête.")
