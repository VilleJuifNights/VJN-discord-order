
import discord.ui
from discord import Interaction

from src.client import VJNInteraction
from src.domain.entity.guildConfig import Category


class OrderTypeButton(discord.ui.Button):

    def __init__(self, category: Category):
        super().__init__(label=category.name, emoji=category.emote, custom_id=f"order_{category.name}")
        self.category = category

    async def callback(self, interaction: VJNInteraction):

        await interaction.response.send_message("test", ephemeral=True)
