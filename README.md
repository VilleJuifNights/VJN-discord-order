# VJN-discord-order

This bot allows you to order crepes and other food during Villejuif nights via Discord

## How does the bot currently works ?

Currently, to use the bot, all you have to do is run the command `/add_button` followed by the id of the channel you want people to order from. This will bring up an order button in the channel you specified. Once clicked, it will create a channel with the order number of the person who will be able to browse the menu, which is still under development at the moment, to make the choice they want.

## How to contribute to the bot ?

### Cloning the repo
```sh
git clone git@github.com:VilleJuifNights/VJN-discord-order.git
```

### Requirements
To run the bot you need to have the discord.py module installed on your computer.
If you didn't installed it, checkout this link : https://github.com/Rapptz/discord.py/tree/master

Moreover, you need to add the id of the channel where you want the commands will be either in a file called "commands_channel.txt" in the same directory or either directly in the code.
Obviously, you also need to add your own bot token either in a file called "token_bot.txt" or either directly in the code.
