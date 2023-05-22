import discord
from discord import app_commands, Game, Activity, ActivityType
from datetime import datetime

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    '''
    show if there is no error and start the RPC
    '''
    print("Ready")
    await tree.sync()
    game = Game(name="/commander")
    activity = Activity(name="Playing", type=ActivityType.playing)
    await client.change_presence(activity=game)

commandes = {}
identifiant = 1

@tree.command(name="commander")
@app_commands.describe(choix="pour commander des trucs bons")
@app_commands.choices(choix=[
    app_commands.Choice(name = "Crèpe usuelle", value = "crèpe usuelle"), 
    app_commands.Choice(name = "Crèpe combinaison", value = "crèpe combinaison"), 
    app_commands.Choice(name = "Churros", value = "churros"), 
    app_commands.Choice(name = "Gauffres", value = "gauffres"), 
    app_commands.Choice(name = "Barbe à papa", value = "barbes à papa"), 
    app_commands.Choice(name = "soda", value = "soda")
    ])
async def commander(interaction: discord.Interaction, choix: app_commands.Choice[str]):
    '''
    to order food
    '''
    global identifiant
    choix = choix.value
    with open("commands_channel.txt", "r") as commands_channel:
        channel = client.get_channel(int(commands_channel.read()))
    people = await interaction.user.create_dm()
    link = ""
    if choix == "soda":
        link = "https://boutique.sofratel.fr/laon/wp-content/uploads/sites/17/2021/12/boissons33cl.jpg"
    title = "Commande n°" + str(identifiant) + "\ncommandé à " + datetime.now().strftime("%H:%M")
    emb = discord.Embed(title=title, description=f"{interaction.user.mention} a commandé des {choix}", color=0x3498db)
    message = discord.Embed(title=title, description=f"Tu a commandé : {choix}", color=0x3498db)
    if (link != ""):
        emb.set_image(url=link)
    await channel.send(embed=emb)
    await people.send(embed=message)
    await people.send("Il faut maintenant que tu viennes au stand pour pouvoir valider et préparer ta commande")
    message_sent = await interaction.response.send_message("Ta commande a bien été enregistré")
    commandes[identifiant] = (choix, people, title, message_sent.position)
    identifiant += 1

@tree.command(name="valider")
@app_commands.describe(nombre="le numéro de la commande que tu veux valider")
async def valider(interaction: discord.Interaction, nombre:int):
    '''
    to validate a command
    '''
    with open("commands_channel.txt", "r") as commands_channel:
        channel = client.get_channel(int(commands_channel.read()))
    real_messages = []
    messages = channel.history(limit=None)
    if len(commandes) > 0:
        async for message in messages:
            real_messages.append(message)
        length = len(real_messages)
        print(real_messages, length)
        if length > 0 and nombre in commandes.keys():
            (_, people, title, location) = commandes[nombre]
            for i in range(length):
                if message[i].position == location:
                    now = datetime.now().strftime("%H:%M")
                    new_emb = discord.Embed(title=title, description=f"Commande n°{nombre} validé par {interaction.user.mention} à {now}", color=0x51ff00)
                    await real_messages[i].edit(embed=new_emb)
                    await people.send(f"Ta commande n°{nombre} a bien été validé et est en préparation.\nNous te renverrons un message lorsque ta commande sera prête")
                    await interaction.response.send_message(f"La commande n°{nombre} a bien été validé")
        else:
            await interaction.response.send_message("Je n'ai pas trouvé de commande portant ce numéro")
    else:
        await interaction.response.send_message("Je n'ai pas trouvé de commande portant ce numéro")

@tree.command(name="add_button")
@app_commands.describe(identifiant="l'identifiant de la channel où mettre le bouton")
async def add_button(interaction: discord.Interaction, identifiant:str):
    channel = client.get_channel(int(identifiant))

    button = discord.ui.Button(style=discord.ButtonStyle.primary, label='Click Me!', custom_id='button_clicked')

    view = discord.ui.View()
    view.add_item(button)

    await channel.send(content='Here is a message with a button:', view=view) 

@tree.command(name="clear")
@app_commands.describe(number="le nombre de message que tu veux supprimer")
async def clear(interaction: discord.Interaction, number : int):
        list_messages = interaction.channel.history(limit = number + 1)
        messages = []

        async for message in list_messages:
            messages.append(message)
        for message in messages:
            await(message.delete())

with open('token_bot.txt', 'r') as token:
    client.run(token.read())
