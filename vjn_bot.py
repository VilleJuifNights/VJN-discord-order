import discord
from discord.ext import commands, tasks
from discord import ApplicationCommandInteraction as APPCI, SlashCommandOptionChoice as Choice, SlashCommandOption as Option, Button, ButtonStyle
from datetime import datetime
from random import choice

bot = commands.Bot(command_prefix="$", sync_commands = True)
client = discord.Client()

@bot.event
async def on_ready():
    '''
    show if there is no error and start the RPC
    '''
    print("ready")
    changeStatus.start()

status = ["/commander"]
commandes = {}
identifiant = 1

@bot.command()
async def start(ctx, secondes = 5):
    '''
    function to display messages stored in the list called status
    '''
    changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
    '''
    if there are several messages to display, it will make it change every 5 seconds
    '''
    game = discord.Game(choice(status))
    await bot.change_presence(activity = game)

@bot.slash_command(name="commander", description = "pour commander des trucs bons", options=[
    Option(name="choix", description="le choix que tu veux faire", option_type=3, required=True, choices=[Choice(name = "Crèpe usuelle", value = "crèpe usuelle"), Choice(name = "Crèpe combinaison", value = "crèpe combinaison"), Choice(name = "Churros", value = "churros"), Choice(name = "Gauffres", value = "gauffres"), Choice(name = "Barbe à papa", value = "barbes à papa"), Choice(name = "soda", value = "soda")])
])
async def commander(ctx:APPCI, choix):
    '''
    to order food
    '''
    global identifiant
    channel = bot.get_channel(1094212525157007410)
    people = await ctx.author.create_dm()
    link = ""
    if choix == "soda":
        link = "https://boutique.sofratel.fr/laon/wp-content/uploads/sites/17/2021/12/boissons33cl.jpg"
    title = "Commande n°" + str(identifiant) + "\ncommandé à " + datetime.now().strftime("%H:%M")
    commandes[identifiant] = (choix, people, title)
    emb = discord.Embed(title=title, description=f"{ctx.author.mention} a commandé des {choix}", color=0x3498db)
    message = discord.Embed(title=title, description=f"Tu a commandé : {choix}", color=0x3498db)
    if (link != ""):
        emb.set_image(url=link)
    await channel.send(embed=emb)
    await people.send(embed=message)
    await people.send("Il faut maintenant que tu viennes au stand pour pouvoir valider et préparer ta commande")
    await ctx.respond("Ta commande a bien été enregistré")
    identifiant += 1

@bot.slash_command(name="valider", description="pour valider une commande", options=[
    Option(name="nombre", description="le numéro de commande à valider", option_type=4, required=True)])
async def valider(ctx:APPCI, nombre):
    '''
    to validate a command
    '''
    channel = bot.get_channel(1094212525157007410)
    messages = await channel.history(limit=200).flatten()
    for message in messages:
        if message.position == nombre:
            (_, people, title) = commandes[nombre]
            now = datetime.now().strftime("%H:%M")
            new_emb = discord.Embed(title=title, description=f"Commande n°{nombre} validé par {ctx.author.mention} à {now}", color=0x51ff00)
            await message.edit(embed=new_emb)
            await people.send(f"Ta commande n°{nombre} a bien été validé et est en préparation.\nNous te renverrons un message lorsque ta commande sera prête")

with open('token_bot.txt', 'r') as token:
    bot.run(token.read())
