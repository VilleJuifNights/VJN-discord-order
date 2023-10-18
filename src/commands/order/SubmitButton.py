import discord.ui
from discord import Interaction, ButtonStyle, Colour

from src.client import VJNInteraction
from src.data.utils import create_order, get_session
from src.domain.entity.Config import Category, Toppings, Choice
from src.domain.service.OrderService import new_order
from uuid import uuid4


class SubmitButton(discord.ui.Button):

    def __init__(self, category: Category, toppings: list[Choice] = None, login: str = None):

        super().__init__(label="Submit", custom_id=f"order_{category.name}_submit_{uuid4()}", style=ButtonStyle.green)
        self.category = category
        self.toppings = toppings or []
        self.login = login

    async def callback(self, interaction: VJNInteraction):
        await interaction.response.defer(ephemeral=True)
        if self.login:
            order = create_order(self.login, self.category, self.toppings)
        else:
            order = create_order(interaction.user, self.category, self.toppings)

        session = get_session()
        session.add(order)
        session.commit()

        embed = discord.Embed(title="Résumé de votre commande", color=Colour.blue())
        embed.add_field(name="Catégorie", value=self.category.name, inline=False)
        if self.toppings:
            embed.add_field(name="Toppings", value="\n".join([topping.name for topping in self.toppings]), inline=False)
        embed.add_field(name="Prix", value=f"{order.total_cost}€" if order.total_cost > 0 else "Gratuit", inline=False)
        embed.set_footer(text=f"Commande #{order.pretty_id}")

        embed.description = "Votre commande a bien été prise en compte !"
        if order.total_cost > 0:
            embed.description += f"\nDirigez vous vers un membre du staff pour payer votre commande."

        await interaction.message.delete()
        await interaction.followup.send(embed=embed)

        await new_order(interaction.client, order)
