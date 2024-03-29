from typing import Tuple

import discord.ui

from src.client import VJNInteraction
from src.commands.order.SubmitButton import SubmitButton
from src.domain.entity.Config import Category, Choice
from uuid import uuid4


class OrderTypeButton(discord.ui.Button):

    def __init__(self, category: Category, selected_choices: list[Choice] = None, login: str = None):
        super().__init__(label=category.name, emoji=category.emote, custom_id=f"order_{category.name}_{uuid4()}",
                         style=discord.ButtonStyle.green)
        self.category = category
        self.selected_choices = selected_choices or []
        self.login = login

    async def callback(self, interaction: VJNInteraction):
        if not self.category.toppings:  # No choices
            embed, view = get_order_ui(self.category, login=self.login)
            embed.add_field(name="Total", value=f"{self.category.price}€")
            await interaction.message.delete()
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await choose_toppings(interaction, self.category, self.selected_choices, self.login)


def get_order_ui(category: Category, selected_choices: list[Choice] = None, login: str = None) \
        -> Tuple[discord.Embed, discord.ui.View]:
    embed = discord.Embed(title="Order", description="Order a meal", color=discord.Color.green())
    embed.add_field(name="Category", value=category.name)

    view = discord.ui.View()
    button = SubmitButton(category=category, toppings=selected_choices, login=login)
    # check if number of choice are between min and max (max can be -1 for unlimited), else disable button
    nb_choices = len(selected_choices or [])
    if (category.toppings.min_choices > nb_choices or nb_choices > category.toppings.max_choices) and category.toppings.max_choices != -1:
        button.disabled = True

    view.add_item(button)

    return embed, view


async def choose_toppings(interaction: VJNInteraction, category: Category, selected_choices: list[Choice] = None,
                          login: str = None):
    """
    Display the choice of toppings for a category
    @param login: Optional login of the user
    @param interaction:  Interaction
    @param category: Category of the order
    @param selected_choices:  List of selected choices
    """
    selected_choices = selected_choices or []
    embed, view = get_order_ui(category, selected_choices, login)

    if selected_choices:
        embed.add_field(name="Toppings", value=", ".join([choice.name for choice in selected_choices]))

    embed.add_field(name="Total", value=f"{category.price + sum([choice.extra for choice in selected_choices])}€")

    opt = [(choice, choice in selected_choices) for choice in category.toppings.options]
    if opt:
        view.add_item(ChoiceSelection("Suppléments", category, opt, True, login=login))

    opt = [(choice, choice in selected_choices) for choice in category.toppings.recommandations]
    if opt:
        view.add_item(ChoiceSelection("Recommandations", category, opt, False, login=login))

    await interaction.message.delete()
    await interaction.response.send_message(embed=embed, view=view)


class ChoiceSelection(discord.ui.Select):

    def __init__(self, placeholder: str, category: Category, choices: list[Tuple[Choice, bool]],
                 multiple_choices: bool, login: str = None):
        """
        Initialize a select box with choices.
        @param placeholder: Name of the select box
        @param category: Category of the order
        @param choices: List of choices to display (with default value : true if selected, false otherwise)
        @param multiple_choices:  True if multiple choices are allowed, false otherwise
        """
        self.category = category
        self.choices = choices
        self.login = login
        min_values = 0
        max_values = min(len(self.choices), 25) if multiple_choices else 1
        super().__init__(placeholder=placeholder, max_values=max_values, min_values=min_values)
        for opt in self.choices:
            choice, default = opt

            self.add_option(label=choice.name, value=choice.name, description=f"+{choice.extra}€",
                            default=default)

    async def callback(self, interaction: VJNInteraction):
        choices = [choice[0] for choice in self.choices if choice[0].name in self.values]

        # get the choice object from the name
        await choose_toppings(interaction, self.category, choices, self.login)
