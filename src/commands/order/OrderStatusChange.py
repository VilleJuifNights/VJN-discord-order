import uuid

import discord
from discord import ButtonStyle, Interaction
from sqlalchemy import select

from src.data.models import Order
from src.data.utils import get_session
from src.domain.entity.OrderStatus import OrderStatus, status_to_button_label, next_status


class ChangeStatusButton(discord.ui.Button):

    def __init__(self, order_id: uuid.UUID, status: OrderStatus, override_label: str = None, staff_id: int = None):
        label = override_label or status_to_button_label(status)
        super().__init__(label=label, custom_id=f"order_{order_id}_{status.name}",
                         style=ButtonStyle.green)
        self.order = order_id
        self.status = status
        self.staff_id = staff_id

    async def callback(self, interaction: Interaction) -> None:
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
        view = discord.ui.View(timeout=None)

        if self.status == OrderStatus.PAYED:
            channel = interaction.client.get_channel(interaction.client.config.settings.validated_channel)
            if channel is None:
                raise Exception(
                    f"Could not find channel with ID {interaction.client.config.settings.validated_channel}")
            await interaction.message.delete()
            for i in range(1, 6):  # hardcoded for now TODO: change this
                button = ChangeStatusButton(self.order, next_status(self.status), f"Attribuer à staff n°{i}", i)
                button.custom_id += f"_{i}"
                view.add_item(button)
            await channel.send(embed=embed, view=view)
            return

        view.add_item(ChangeStatusButton(self.order, next_status(self.status), staff_id=self.staff_id))

        if self.status == OrderStatus.IN_PROGRESS:
            # send message to user
            embed.add_field(name="Staff en charge", value=f"Staff n°{self.staff_id}")
            try:
                user = await interaction.client.fetch_user(int(order.user_id))
                await user.send(
                    f"Votre commande #{order.pretty_id} est en cours de préparation et sera bientôt prête !")
            except discord.NotFound or discord.Forbidden:
                await interaction.followup.send(f"Impossible de contacter l'utilisateur {order.user_id} pour lui "
                                                f"annoncer que sa commande #{order.pretty_id} est en cours de "
                                                f"préparation.")

        await interaction.message.edit(embed=embed, view=view)

        if self.status == OrderStatus.COMPLETED:
            # send message to user
            try:
                user = await interaction.client.fetch_user(int(order.user_id))
                await user.send(f"Votre commande #{order.pretty_id} est prête !")
            except discord.NotFound or discord.Forbidden:
                await interaction.followup.send(f"Impossible de contacter l'utilisateur {order.user_id} pour lui "
                                                f"annoncer que sa commande #{order.pretty_id} est prête.")
