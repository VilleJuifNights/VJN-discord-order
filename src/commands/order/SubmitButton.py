import discord.ui
from discord import Interaction, ButtonStyle

from src.client import VJNInteraction
from src.domain.entity.Config import Category, Toppings, Choice


class SubmitButton(discord.ui.Button):

    def __init__(self, category: Category, toppings: list[Choice] = None):
        super().__init__(label="Submit", custom_id=f"order_{category.name}_submit", style=ButtonStyle.green)
        self.category = category
        self.toppings = toppings or []

    async def callback(self, interaction: VJNInteraction):
        if self.toppings:
            message = f"Order {self.category.name} with {', '.join([topping.name for topping in self.toppings])}"
        else:
            message = f"Order {self.category.name}"
        await interaction.response.send_message(message, ephemeral=True)
