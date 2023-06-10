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
identifiant_commande = 1

@tree.command(name="order")
@app_commands.describe(choix="pour commander des trucs bons")
@app_commands.choices(choix=[
    app_commands.Choice(name = "Crèpe usuelle", value = "crèpe usuelle"), 
    app_commands.Choice(name = "Crèpe combinaison", value = "crèpe combinaison"), 
    app_commands.Choice(name = "Churros", value = "churros"), 
    app_commands.Choice(name = "Gauffres", value = "gauffres"), 
    app_commands.Choice(name = "Barbe à papa", value = "barbes à papa"), 
    app_commands.Choice(name = "soda", value = "soda")
    ])
async def order(interaction: discord.Interaction, choix: app_commands.Choice[str]):
    '''
    to order food
    '''
    global identifiant_commade
    choix = choix.value
    with open("commands_channel.txt", "r") as commands_channel:
        channel = client.get_channel(int(commands_channel.read()))
    people = await interaction.user.create_dm()
    link = ""
    if choix == "soda":
        link = "https://boutique.sofratel.fr/laon/wp-content/uploads/sites/17/2021/12/boissons33cl.jpg"
    title = "Commande n°" + str(identifiant_commande) + "\ncommandé à " + datetime.now().strftime("%H:%M")
    emb = discord.Embed(title=title, description=f"{interaction.user.mention} a commandé des {choix}", color=0x3498db)
    message = discord.Embed(title=title, description=f"Tu a commandé : {choix}", color=0x3498db)
    if (link != ""):
        emb.set_image(url=link)
    await channel.send(embed=emb)
    await people.send(embed=message)
    await people.send("Il faut maintenant que tu viennes au stand pour pouvoir valider et préparer ta commande")
    message_sent = await interaction.response.send_message("Ta commande a bien été enregistré")
    commandes[identifiant_commande] = (choix, people, title, message_sent.position)
    identifiant_commande += 1

@tree.command(name="validate")
@app_commands.describe(nombre="le numéro de la commande que tu veux valider")
async def validate(interaction: discord.Interaction, nombre:int):
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
async def add_button(interaction: discord.Interaction, identifiant: str):
    channel = client.get_channel(int(identifiant)) 

    async def usuelle_callback(interaction : discord.Interaction):
        nutella = discord.ui.Button(style=discord.ButtonStyle.primary, label="nutella", custom_id="nutella")
        specullos = discord.ui.Button(style=discord.ButtonStyle.primary, label="spécullos", custom_id="specullos")
        sucre = discord.ui.Button(style=discord.ButtonStyle.primary, label="sucre", custom_id="sucre")
        emmJamb = discord.ui.Button(style=discord.ButtonStyle.primary, label="emmental-jambon", custom_id="emmJamb")
        emmPoul = discord.ui.Button(style=discord.ButtonStyle.primary, label="emmental-poulet", custom_id="emmPoul")
        
        ingredients = [nutella, specullos, sucre, emmJamb, emmPoul]

        usuelle_view = discord.ui.View()
        for elt in ingredients:
            uselle_view.add_item(elt)

    async def crepe_callback(interaction : discord.Interaction):
        usuelle = discord.ui.Button(style=discord.ButtonStyle.primary, label="Crêpe usuelle", custom_id="usuelle")
        usuelle.callback = usuelle_callback
        combinaison = discord.ui.Button(style=discord.ButtonStyle.primary, label="Crêpe combinaison", custom_id="combinaison")
        crepe_view = discord.ui.View()
        crepe_view.add_item(usuelle)
        crepe_view.add_item(combinaison)
        
        await interaction.response.send_message("Choisis le type de crêpe que tu veux", view=crepe_view)

    async def cancel_callback(interaction : discord.Interaction):
        guild = interaction.guild
        index = 0

        while index < len(guild.channels) and guild.channels[index].name != "commande_" + str(identifiant_commande):
           index += 1
        await guild.channels[index].delete()
        await interaction.response.send_message("Votre commande a bien été annulé", ephemeral=True)

    async def button_callback(interaction: discord.Interaction):
        guild = interaction.guild
        new_channel_name = "commande_" + str(identifiant_commande)
        new_channel = await guild.create_text_channel(new_channel_name)

        crepe = discord.ui.Button(style=discord.ButtonStyle.primary, label='Crêpe', custom_id="crepe")
        churros = discord.ui.Button(style=discord.ButtonStyle.primary, label='Churros', custom_id="churros")
        gauffres = discord.ui.Button(style=discord.ButtonStyle.primary, label='Gauffres', custom_id="gauffres")
        BarbePapa = discord.ui.Button(style=discord.ButtonStyle.primary, label='Barbe à papa', custom_id="BarbePapa")
        soda = discord.ui.Button(style=discord.ButtonStyle.primary, label='Soda', custom_id="soda")
        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label='annuler la commande', custom_id="cancel")
        buttons = [crepe, churros, gauffres, BarbePapa, soda, cancel]
        new_view = discord.ui.View()
        for elt in buttons:
            if elt.custom_id == "crepe":
                elt.callback = crepe_callback
            elif elt.custom_id == "cancel":
                elt.callback = cancel_callback
            new_view.add_item(elt)
        await new_channel.send(content='Choisis ce que tu veux prendre parmi les bouttons ci-dessous', view=new_view)

    button = discord.ui.Button(style=discord.ButtonStyle.primary, label='Click Me!', custom_id='button_clicked')
    button.callback = button_callback

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
