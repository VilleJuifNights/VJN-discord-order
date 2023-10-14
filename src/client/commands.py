from discord.app_commands import Command

from src import commands

commands = [
    {'command': Command(name="order", description="Order a meal", callback=commands.order)},
    {'command': Command(name="cancel", description="Cancel your order", callback=commands.cancel)},
    {'command': Command(name="status", description="Get your order status", callback=commands.status)},
]
