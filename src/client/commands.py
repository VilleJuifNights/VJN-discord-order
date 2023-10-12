from discord.app_commands import Command

from src.actions import orders

commands = [
    {'command': Command(name="order", description="Order a meal", callback=orders.order)},
    {'command': Command(name="cancel", description="Cancel your order", callback=orders.cancel)},
    {'command': Command(name="status", description="Get your order status", callback=orders.status)},
]
