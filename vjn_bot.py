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
    game = Game(name="/order")
    activity = Activity(name="Playing", type=ActivityType.playing)
    await client.change_presence(activity=game)

commandes = {}
identifiant_commande = 1
start_commande = 0

####################################################################### 
############### les lignes commentés ci-dessous étaient ################
############## juste des tests pour que je sache comment ###############
################### commencer a implémenter le bot #####################
#######################################################################

"""@tree.command(name="order")
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
    global identifiant_commande
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
        await interaction.response.send_message("Je n'ai pas trouvé de commande portant ce numéro")"""

##################################################################################### fin de mes tests du debut pour comprendre ################
#################### comment implementer le bot ########################
########################################################################

def prettyDisplay(liste):
    '''
    affiche la commande du joueur chaque qu'il fait un choix
    '''
    unique = []
    output = []
    contenu = ""
    for elt in liste:
        if elt not in unique:
            unique.append(elt)
            output.append((liste.count(elt), elt))
    for (num, elt) in sorted(output, key=lambda x: x[1]):
        contenu += f"- {elt} : {num}\n"
    emb = discord.Embed(title="Votre commande actuelle", description=contenu, color=0x3498db)
    return emb

@tree.command(name="add_button", description="ajouter le bouton pour que les clients commandent")
@app_commands.describe(identifiant="l'identifiant de la channel où mettre le bouton")
async def add_button(interaction: discord.Interaction, identifiant: str):
    channel = client.get_channel(int(identifiant))
    start_commande = int(identifiant)

    async def button_callback(interaction: discord.Interaction):
        guild = interaction.guild
        global crepe_combinaison, commande
        crepe_combinaison = []
        commande = []
        new_channel_name = "commande_" + str(identifiant_commande)
        new_channel = guild.channels[2]
        if interaction.channel_id == start_commande:
            already = False
            for channel in guild.channels:
                if channel.name == new_channel_name:
                    already = True
            if not already:
                new_channel = await guild.create_text_channel(new_channel_name)
                await interaction.response.send_message(content=f"Le channel {new_channel.mention} vient d'être créer pour t'aider à commander", ephemeral=True)
            else: 
                await interaction.response.send_message(f"Tu as déjà lancé une commande. Pour continuer à commander, il te suffit d'aller au channel: {channel.mention}", ephemeral=True)
        else:
            new_channel = client.get_channel(interaction.channel_id)
            list_messages = interaction.channel.history(limit = 1)
            messages = []
        
            async for message in list_messages:
                messages.append(message)

            if len(messages) > 0:
                for message in messages:
                    await(message.delete())


        crepe = discord.ui.Button(style=discord.ButtonStyle.primary, label='Crêpe', custom_id="Crepe")
        churros = discord.ui.Button(style=discord.ButtonStyle.primary, label='Churros', custom_id="Churros")
        gauffres = discord.ui.Button(style=discord.ButtonStyle.primary, label='Gauffres', custom_id="Gauffres")
        BarbePapa = discord.ui.Button(style=discord.ButtonStyle.primary, label='Barbe à papa', custom_id="Barbe à papa")
        soda = discord.ui.Button(style=discord.ButtonStyle.primary, label='Soda', custom_id="Soda")
        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label='annuler la commande', custom_id="cancel")
        buttons = [crepe, churros, gauffres, BarbePapa, soda, cancel]
        new_view = discord.ui.View()
        for elt in buttons:
            if elt.custom_id == "Crepe":
                elt.callback = crepe_callback
            elif elt.custom_id == "cancel":
                elt.callback = cancel_callback
            else:
                elt.callback = lambda i=interaction, s=elt.custom_id: show_callback(i, s)
            new_view.add_item(elt)
        await new_channel.send(content='Choisis ce que tu veux prendre parmi les boutons ci-dessous', view=new_view)

    
    async def crepe_callback(interaction : discord.Interaction):
        '''
        affiche le menu des crepes
        '''
        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())


        usuelle = discord.ui.Button(style=discord.ButtonStyle.primary, label="Crêpe usuelle", custom_id="usuelle")
        usuelle.callback = usuelle_callback
        
        combinaison = discord.ui.Button(style=discord.ButtonStyle.primary, label="Crêpe combinaison", custom_id="combinaison")
        combinaison.callback = combinaison_callback
        
        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="Revenir au choix précédent", custom_id="back")
        back.callback = button_callback
        
        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback
        
        crepe_view = discord.ui.View()
        crepe_view.add_item(usuelle)
        crepe_view.add_item(combinaison)
        crepe_view.add_item(back)
        crepe_view.add_item(cancel)

        await interaction.response.send_message("Choisis le type de crêpe que tu veux", view=crepe_view)
    
    async def show_callback(interaction : discord.Interaction, information):
        '''
        montre la commande de l'utilisateur chaque fois au'il fait un choix
        '''
        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())

        commande.append(information)

        continuer = discord.ui.Button(style=discord.ButtonStyle.primary, label="continuer de commander", custom_id="continue")
        continuer.callback = button_callback

        confirm = discord.ui.Button(style=discord.ButtonStyle.primary, label="terminer et confirmer la commande", custom_id="confirm")

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        commande_view = discord.ui.View()
        commande_view.add_item(continuer)
        commande_view.add_item(confirm)
        commande_view.add_item(cancel)

        await interaction.response.send_message("Que voulez-vous faire ?", embed=prettyDisplay(commande), view=commande_view)
    
    async def usuelle_callback(interaction : discord.Interaction):
        '''
        montre le menu des crepes usuelles
        '''
        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())

        typeCrepe = "Crêpe usuelle "
        nutella = discord.ui.Button(style=discord.ButtonStyle.primary, label="nutella", custom_id=typeCrepe + "nutella")
        specullos = discord.ui.Button(style=discord.ButtonStyle.primary, label="spéculos", custom_id=typeCrepe + "spéculos")
        sucre = discord.ui.Button(style=discord.ButtonStyle.primary, label="sucre", custom_id= typeCrepe + "sucre")
        emmJamb = discord.ui.Button(style=discord.ButtonStyle.primary, label="emmental-jambon", custom_id=typeCrepe + "emmJamb")
        emmPoul = discord.ui.Button(style=discord.ButtonStyle.primary, label="emmental-poulet", custom_id=typeCrepe + "emmPoul")
        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="revenir au choix précédent", custom_id="back")
        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")

        ingredients = [nutella, specullos, sucre, emmJamb, emmPoul, back, cancel]

        usuelle_view = discord.ui.View()
        for elt in ingredients:
            if elt.custom_id == "back":
                elt.callback = crepe_callback
            elif elt.custom_id == "cancel":
                elt.callback = cancel_callback
            else:
                elt.callback = lambda i=interaction, s=typeCrepe + elt.label: show_callback(i, s)
            usuelle_view.add_item(elt)

        await interaction.response.send_message("Choisis l'ingrédient que tu veux dans ta crêpe", view=usuelle_view)

    
    async def combinaison_callback(interaction : discord.Interaction):
        '''
        montre le menu des crepes combinaisons
        '''
        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())

        sucre = discord.ui.Button(style=discord.ButtonStyle.primary, label="Crêpe sucré", custom_id="sucre")
        sucre.callback = sucre_callback
        
        sel = discord.ui.Button(style=discord.ButtonStyle.primary, label="Crêpe salé", custom_id="sel")
        sel.callback = sale_callback

        if crepe_combinaison == []:
            back = discord.ui.Button(style=discord.ButtonStyle.primary, label="revenir au choix précédent", custom_id="back")
            back.callback = crepe_callback
        else:
            finish = discord.ui.Button(style=discord.ButtonStyle.primary, label="finir la crêpe combinaison en cours", custom_id="finish")
            finish.callback = lambda i=interaction, s="crêpe combinaison:["+", ".join(crepe_combinaison)+"]":show_callback(i, s)

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        combinaison_view = discord.ui.View()
        
        combinaison_view.add_item(sucre)
        combinaison_view.add_item(sel)
        if crepe_combinaison == []:
            combinaison_view.add_item(back)
        else:
            combinaison_view.add_item(finish)
        combinaison_view.add_item(cancel)

        await interaction.response.send_message("Veuillez choisir le type de crêpe combinaison que vous voulez", view=combinaison_view)


    async def sale_callback(interaction : discord.Interaction):
        '''
        montre le menu des crepes combinaisons salées
        '''

        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())

        emb = discord.Embed(title="Les ingrédients possibles pour une crêpe salé", color=0x3498db)
        emb.add_field(name="1 euro", value="- Emmental\n- Chèvre\n- Poulet\n- Jambon\n- Viande hachée\n- Thon\n- Saucisson")
        emb.add_field(name="50 centimes", value="- Crème fraîche\n- Oignon\n- œuf\n- Champignon\n- Salade\n- Tomate")
        emb.add_field(name="gratuit", value="- Chantilly\n- Citron\n- Beurre\n- Toping")

        un_euro = discord.ui.Button(style=discord.ButtonStyle.primary, label="1 euro", custom_id="un_euro")
        un_euro.callback = un_euro_sale_callback

        cinquante_cent = discord.ui.Button(style=discord.ButtonStyle.primary, label="50 centimes", custom_id="cinquante_cent")
        cinquante_cent.callback = cinquante_cent_sale_callback

        gratos = discord.ui.Button(style=discord.ButtonStyle.primary, label="gratuit", custom_id="gratos")
        gratos.callback = lambda i=interaction, current="sel":gratos_callback(i, current)

        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="revenir au choix précédent", custom_id="back")
        back.callback = combinaison_callback

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        sale_view = discord.ui.View()

        sale_view.add_item(un_euro)
        sale_view.add_item(cinquante_cent)
        sale_view.add_item(gratos)
        sale_view.add_item(back)
        sale_view.add_item(cancel)

        await interaction.response.send_message("Choisis les ingrédients que tu veux ajouter à ta crêpe", embed=emb, view=sale_view) 
    
    async def un_euro_sale_callback(interaction : discord.Interaction):
        '''
        montre le menu des ingredients des crepes combinaisons salees a un euro
        '''

        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())
        
        emmental = discord.ui.Button(style=discord.ButtonStyle.primary, label="Emmental", custom_id="emmental")

        chevre = discord.ui.Button(style=discord.ButtonStyle.primary, label="Chèvre", custom_id="chevre")

        poulet = discord.ui.Button(style=discord.ButtonStyle.primary, label="Poulet", custom_id="Poulet")

        jambon = discord.ui.Button(style=discord.ButtonStyle.primary, label="Jambon", custom_id="jambon")

        minced = discord.ui.Button(style=discord.ButtonStyle.primary, label="Viande hachée", custom_id="minced")

        thon = discord.ui.Button(style=discord.ButtonStyle.primary, label="Thon", custom_id="thon")

        saucisson = discord.ui.Button(style=discord.ButtonStyle.primary, label="Saucisson", custom_id="saucisson")
        
        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="revenir au choix précédent", custom_id="back")
        back.callback = sale_callback

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        ingredients = [emmental, chevre, poulet, jambon, minced, thon, saucisson, back, cancel]

        un_euro_sale_view = discord.ui.View()
        for elt in ingredients:
            if elt != back and elt != cancel:
                elt.callback = lambda i=interaction, ingredient=elt.label:add_ingredient_to_crepe_combinaison(i, ingredient)
            un_euro_sale_view.add_item(elt)

        await interaction.response.send_message("Choisis l'ingredient que tu veux ajouter à ta crêpe", view=un_euro_sale_view)
    
    async def cinquante_cent_sale_callback(interaction : discord.Interaction):
        '''
        montre le menu des ingredients des crepes combinaisons salees a cinquante centimes
        '''
        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())

        freshCream = discord.ui.Button(style=discord.ButtonStyle.primary, label="Crème fraîche", custom_id="freshCream")

        onion = discord.ui.Button(style=discord.ButtonStyle.primary, label="Oignon", custom_id="onion")

        egg = discord.ui.Button(style=discord.ButtonStyle.primary, label="œuf", custom_id="egg")

        mushroom = discord.ui.Button(style=discord.ButtonStyle.primary, label="Champignon", custom_id="mushroom")

        salad = discord.ui.Button(style=discord.ButtonStyle.primary, label="Salade", custom_id="salad")

        tomato = discord.ui.Button(style=discord.ButtonStyle.primary, label="Tomate", custom_id="Tomate")

        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="retourner à l'étape précédente", custom_id="back")
        back.callback = sale_callback

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        ingredients = [freshCream, onion, egg, mushroom, salad, tomato, back, cancel]

        cinquante_cent_sale_view = discord.ui.View()

        for elt in ingredients:
            if elt != back and elt != cancel:
                elt.callback = lambda i=interaction, ingredient=elt.label:add_ingredient_to_crepe_combinaison(i, ingredient)

            cinquante_cent_sale_view.add_item(elt)

        await interaction.response.send_message("Choisis l'ingrédient que tu veux ajouter à ta crêpe", view=cinquante_cent_sale_view)

    async def sucre_callback(interaction : discord.Interaction):
        '''
        montre le menu des crepes combinaisons sucres
        '''

        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())

        emb = discord.Embed(title="Les ingrédients possibles pour une crêpe sucré", color=0x3498db)
        emb.add_field(name="1 euro", value="- Sirop d'érable\n- Beurre de cacahuète\n- Nutella\n- Milka\n- Spéculoos\n- Fraise (le fruit)\n- confiture d'Abricot\n- Miel\n- Caramel")
        emb.add_field(name="50 centimes", value="- Confiture de fraise/abricot\n- Banane")
        emb.add_field(name="gratuit", value="- Chantilly\n- Citron\n- Beurre\n- Toping")
        
        un_euro = discord.ui.Button(style=discord.ButtonStyle.primary, label="1 euro", custom_id="un_euro")
        un_euro.callback = un_euro_sucre_callback

        cinquante_cent = discord.ui.Button(style=discord.ButtonStyle.primary, label="50 centimes", custom_id="cinquante_cent")
        cinquante_cent.callback = cinquante_cent_sucre_callback

        gratos = discord.ui.Button(style=discord.ButtonStyle.primary, label="gratuit", custom_id="gratos")
        gratos.callback = lambda i=interaction, current="sucre":gratos_callback(i, current)

        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="revenir au choix précédent", custom_id="back")
        back.callback = combinaison_callback

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        sucre_view = discord.ui.View()

        sucre_view.add_item(un_euro)
        sucre_view.add_item(cinquante_cent)
        sucre_view.add_item(gratos)
        sucre_view.add_item(back)
        sucre_view.add_item(cancel)

        await interaction.response.send_message("Choisis les ingrédients que tu veux ajouter à ta crêpe", embed=emb, view=sucre_view) 

    async def un_euro_sucre_callback(interaction : discord.Interaction):
        '''
        montre le menu des ingredients des crepes combinaisons sucres a un euro
        '''
        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())
        
        maple_syrup = discord.ui.Button(style=discord.ButtonStyle.primary, label="Sirop d'érable", custom_id="Sirop d'érable")

        peanut_butter = discord.ui.Button(style=discord.ButtonStyle.primary, label="Beurre de cacahuète", custom_id="Beurre de cacahuète")

        nutella = discord.ui.Button(style=discord.ButtonStyle.primary, label="Nutella", custom_id="Nutella")

        milka = discord.ui.Button(style=discord.ButtonStyle.primary, label="Milka", custom_id="Milka")

        speculoos = discord.ui.Button(style=discord.ButtonStyle.primary, label="Spéculoos", custom_id="Spéculoos")

        strawberry = discord.ui.Button(style=discord.ButtonStyle.primary, label="Fraise (le fruit)", custom_id="Fraise (le fruit)")

        apricot_jam = discord.ui.Button(style=discord.ButtonStyle.primary, label="Confiture d'abricot", custom_id="Confiture d'abricot")

        honey = discord.ui.Button(style=discord.ButtonStyle.primary, label="Miel", custom_id="Miel")

        caramel = discord.ui.Button(style=discord.ButtonStyle.primary, label="Caramel", custom_id="Caramel")
        
        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="revenir au choix précédent", custom_id="back")
        back.callback = sucre_callback

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        ingredients = [maple_syrup, peanut_butter, nutella, milka, speculoos, strawberry, apricot_jam, honey, caramel, back, cancel]

        un_euro_sucre_view = discord.ui.View()
        for elt in ingredients:
            if elt != back and elt != cancel:
                elt.callback = lambda i=interaction, ingredient=elt.label:add_ingredient_to_crepe_combinaison(i, ingredient)

            un_euro_sucre_view.add_item(elt)

        await interaction.response.send_message("Choisis l'ingredient que tu veux ajouter à ta crêpe", view=un_euro_sucre_view)

    async def cinquante_cent_sucre_callback(interaction : discord.Interaction):
        '''
        montre le menu des ingredients des crepes combinaisons sucres a cinquante centimes
        '''
        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())
        
        strawb_apric_jam = discord.ui.Button(style=discord.ButtonStyle.primary, label="Confiture de fraise/abricot", custom_id="strawb_apric_jam")

        banana = discord.ui.Button(style=discord.ButtonStyle.primary, label="Banane", custom_id="Banane")

        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="revenir au choix précédent", custom_id="back")
        back.callback = sucre_callback

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        ingredients = [strawb_apric_jam, banana, back, cancel]

        cinquante_cent_sucre_view = discord.ui.View()
        for elt in ingredients:
            if elt != back and elt != cancel:
                elt.callback = lambda i=interaction, ingredient=elt.label:add_ingredient_to_crepe_combinaison(i, ingredient)

            cinquante_cent_sucre_view.add_item(elt)

        await interaction.response.send_message("Choisis l'ingredient que tu veux ajouter à ta crêpe", view=cinquante_cent_sucre_view)


    async def gratos_callback(interaction : discord.Interaction, before):
        '''
        montre le menu des ingredients des crepes combinaisons gratuit
        '''
        list_messages = interaction.channel.history(limit = 1)
        messages = []
        
        async for message in list_messages:
            messages.append(message)

        if len(messages) > 0:
           for message in messages:
               await(message.delete())

        chantilly = discord.ui.Button(style=discord.ButtonStyle.primary, label="Chantilly", custom_id="chantilly")

        lemon = discord.ui.Button(style=discord.ButtonStyle.primary, label="Citron", custom_id="Citron")

        butter = discord.ui.Button(style=discord.ButtonStyle.primary, label="Beurre", custom_id="Beurre")

        toping = discord.ui.Button(style=discord.ButtonStyle.primary, label="Toping", custom_id="Toping")

        back = discord.ui.Button(style=discord.ButtonStyle.primary, label="retourner à l'étape précédente", custom_id="back")
        if before == "sel":
            back.callback = sale_callback
        else:
            back.callback = sucre_callback

        cancel = discord.ui.Button(style=discord.ButtonStyle.primary, label="annuler la commande", custom_id="cancel")
        cancel.callback = cancel_callback

        ingredients = [chantilly, lemon, butter, toping, back, cancel]

        gratos_view = discord.ui.View()

        for elt in ingredients:
            if elt != back and elt != cancel:
                elt.callback = lambda i=interaction, ingredient=elt.label:add_ingredient_to_crepe_combinaison(i, ingredient)
            gratos_view.add_item(elt)

        await interaction.response.send_message("Choisis l'ingrédient que tu veux ajouter à ta crêpe", view=gratos_view)

    async def add_ingredient_to_crepe_combinaison(interaction : discord.Interaction, ingredient):
        crepe_combinaison.append(ingredient)
        print(crepe_combinaison)
        await combinaison_callback(interaction)
        await interaction.followup.send(ingredient + " a bien ete ajouté à ta crêpe combinaison", ephemeral=True)



    async def cancel_callback(interaction : discord.Interaction):
        '''
        annule la commande en cours
        '''
        guild = interaction.guild
        index = 0
        commande = []

        while index < len(guild.channels) and guild.channels[index].name != "commande_" + str(identifiant_commande):
           index += 1
        await guild.channels[index].delete()
        await interaction.response.send_message("Votre commande a bien été annulé", ephemeral=True)

    
    button = discord.ui.Button(style=discord.ButtonStyle.primary, label='Commande ici!', custom_id='button_clicked')
    button.callback = button_callback

    view = discord.ui.View(timeout=None)
    view.add_item(button)

    await channel.send(content='Pour commander, veuillez cliquer sur le bouton ci-dessous:', view=view)



@tree.command(name="clear")
@app_commands.describe(number="le nombre de message que tu veux supprimer")
async def clear(interaction: discord.Interaction, number : int):
    '''
    une commande slash pour nous aider si on veut effacer rapidement plusieurs messages a la fois
    '''
    list_messages = interaction.channel.history(limit = number + 1)
    messages = []

    async for message in list_messages:
        messages.append(message)
    for message in messages:
        await(message.delete())



with open('token_bot.txt', 'r') as token:
    client.run(token.read())
