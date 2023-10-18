from discord.app_commands import Command

from src import commands

commands = [
    {'command': Command(name="order", description="Order a meal", callback=commands.order)},
    # {'command': Command(name="cancel", description="Cancel your order", callback=commands.cancel)},
    {'command': Command(name="status", description="Get your order status", callback=commands.status)},
    {'command': Command(name="create", description="Create a new order (staff only)", callback=commands.create),
     "guilds": [1033684799912677388, 890357045138690108]},
    {'command': Command(name="init_message", description="Initialize the message to order a meal (staff only)",
                        callback=commands.init_message),
     "guilds": [1033684799912677388, 890357045138690108]},
    {'command': Command(name="remove_product",
                        description="Remove a product or a topping available in the menu (staff only)",
                        callback=commands.remove_product),
     "guilds": [1033684799912677388, 890357045138690108]
     },
    # {'command': Command(name="add_product", description="Add a product or a topping available in the menu (staff only)", callback=commands.add_product)},
    # {'command': Command(name="init", description="Initialize the button to order a meal (staff only)", callback=commands.init)},
    # {'command': Command(name="stand_status", description="Close/Open the shop (staff only)", callback=commands.close_shop)},
]
