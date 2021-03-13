#DISCLAIMER: Tons of bugs should be expected as well as things that don't make any sense.

#Import Libraries
import discord
import random
import asyncio
import math
import time
import os
import pandas as pd

client = discord.Client()
programDirectory = os.path.dirname(os.path.realpath(__file__))
runProgramUpdate = 0

#Import Pokemon Data
pokemonDataSet = pd.read_csv(programDirectory + "/Resources/CSV/Pokemon.csv")
pokemonMovesDataSet = pd.read_csv(programDirectory + "/Resources/CSV/Moves.csv")
pokemonTypeEffectivenessDataSet = pd.read_csv(programDirectory + "/Resources/CSV/TypeEffectiveness.csv")
pokemonData = pokemonDataSet[['Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Type 1', 'Type 2']].values.tolist()
pokemonMoves = pokemonMovesDataSet[['identifier', 'type_id', 'power', 'pp', 'accuracy', 'priority', 'damage_class_id']].values.tolist() 
pokemonTypeEffectiveness = pokemonTypeEffectivenessDataSet[['damage_type_id', 'target_type_id' ,'damage_factor']].values.tolist()

#Open and apply Discord Bot Token
#MAKE SURE THE BOT TOKEN IS IN botToken.txt!!
with open(programDirectory + '/Resources/botToken.txt', 'r') as file:
    botToken = file.read()
    file.close()

#Define Useful Functions
#converts a input string to a unicode emoji
def wordToEmoji(string):
    if string == 'red':
        return '🔴'
    elif string == 'blue':
        return '🔵'
    elif string == 'yellow':
        return '🟡'
    elif string == 'green':
        return '🟢'
    elif string == 'back':
        return '⬅'
    elif string == 'check':
        return '✔️'
    elif string == 'x':
        return '❌'
    else:
        return None

#determines if a move is super effective, not very effective, or normal.
def getTypeEffectiveness(moveTypeID, targetTypeID):
    for i in pokemonTypeEffectiveness:
        if i[0] == moveTypeID:
            if i[1] == targetTypeID:
                return (i[2] / 100) #dataset has entries as either 50, 100, or 200. this converts it to 0.5, 1, or 2 instead.
    return None

#Convert the Text Representation of Pokemon Types to a Numerical Representation
#Representation may seem random, but it actually is made to match up with the movest dataset
def convert_type_to_num(typeText): #Change the following 2 functions to a more useful python format in the future
    if typeText == 'Fairy': 
        return 18
    elif typeText == 'Normal':
        return 1
    elif typeText == 'Fire':
        return 10
    elif typeText == 'Water':
        return 11
    elif typeText == 'Electric':
        return 13
    elif typeText == 'Grass':
        return 12
    elif typeText == 'Flying':
        return 3
    elif typeText == 'Rock':
        return 6
    elif typeText == 'Steel':
        return 9
    elif typeText == 'Ground':
        return 5
    elif typeText == 'Bug':
        return 7
    elif typeText == 'Poison':
        return 4
    elif typeText == 'Ice':
        return 15
    elif typeText == 'Fighting':
        return 2
    elif typeText == 'Psychic':
        return 14
    elif typeText == 'Dark':
        return 17
    elif typeText == 'Ghost':
        return 8
    elif typeText == 'Dragon':
        return 16
    else:
        return 0

#Convert the Numerical Representation of Pokemon Types to a Text Representation
#Representation may seem random, but it actually is made to match up with the movest dataset
def convert_num_to_type(typeNum):
    if typeNum == 18:
        return 'Fairy'
    elif typeNum == 1:
        return 'Normal'
    elif typeNum == 10:
        return 'Fire'
    elif typeNum == 11:
        return 'Water'
    elif typeNum == 13:
        return 'Electric'
    elif typeNum == 12:
        return 'Grass'
    elif typeNum == 3:
        return 'Flying'
    elif typeNum == 6:
        return 'Rock'
    elif typeNum == 9:
        return 'Steel'
    elif typeNum == 5:
        return 'Ground'
    elif typeNum == 7:
        return 'Bug'
    elif typeNum == 4:
        return 'Poison'
    elif typeNum == 15:
        return 'Ice'
    elif typeNum == 2:
        return 'Fighting'
    elif typeNum == 14:
        return 'Psychic'
    elif typeNum == 17:
        return 'Dark'
    elif typeNum == 8:
        return 'Ghost'
    elif typeNum == 16:
        return 'Dragon'
    else:
        return 0

#Convert the move data entrys to a more readable display format
def moveEntryToName(dataEntry): 
    strings = dataEntry.split("-")
    j = 1
    finalString = ""
    for i in strings:
        finalString = finalString + i.capitalize()
        if j != len(strings):
            finalString = finalString + " "
            j = j + 1
    return finalString

def pkmnNameEntryToName(dataEntry):
    newString = ""
    capitalNumber = 0
    for i in dataEntry:
        if ord(i) < 91 and capitalNumber == 0:
            capitalNumber = capitalNumber + 1
            newString = newString + i
        elif ord(i) < 91 and capitalNumber > 0 and capitalNumber < 2:
            capitalNumber = capitalNumber + 1
            newString = newString + ' (' + i
        else:
            newString = newString + i
    if capitalNumber > 1:
        newString = newString + ')'
    return newString

#Define Classes
class pokemonMove:
    Name = None
    EntryNumber = None
    Type = None
    Power = None
    PPCurrent = None
    PPTotal = None
    Accuracy = None
    Priority = None

class Pokemon:
    Name = None
    Level = None
    TypeOne = None
    TypeTwo = None
    TotalHP = None #Calculated based on HP formula
    CurrentHP = None
    HP = None #Base HP Modifier
    Attack = None
    Defense = None
    SpAtk = None
    SpDef = None
    Speed = None
    MoveOne = pokemonMove()
    MoveTwo = pokemonMove()
    MoveThree = pokemonMove()
    MoveFour = pokemonMove()

    def selectNewPokemon(self, baseLevel):
        pokemonEntryNumber = random.randrange(len(pokemonData))
        self.Level = random.randint(baseLevel - 2, baseLevel + 2) #Modify to add or subract up to 2 from this number
        self.Name = pkmnNameEntryToName(pokemonData[pokemonEntryNumber][0])
        self.HP = pokemonData[pokemonEntryNumber][1]
        self.Attack = pokemonData[pokemonEntryNumber][2]
        self.Defense = pokemonData[pokemonEntryNumber][3]
        self.TotalHP = math.floor(0.01 * (2 * self.HP) * self.Level) + self.Level + 50 #This formula calculates the HP of a given pokemon
        self.CurrentHP = self.TotalHP #Set to max health upon initial selection
        self.SpAtk = pokemonData[pokemonEntryNumber][4]
        self.SpDef = pokemonData[pokemonEntryNumber][5]
        self.Speed = pokemonData[pokemonEntryNumber][6]
        self.TypeOne = pokemonData[pokemonEntryNumber][7]
        self.TypeTwo = pokemonData[pokemonEntryNumber][8]
        self.pickRandomMove(self.MoveOne)
        self.pickRandomMove(self.MoveTwo)
        self.pickRandomMove(self.MoveThree)
        self.pickRandomMove(self.MoveFour)

    def pickRandomMove(self, moveNum): #this will need to be changed so that only relevant moves are selected
        while(1):
            randomMove = random.randrange(len(pokemonMoves))
            if pokemonMoves[randomMove][6] == 2: #The randomly selected move needs to be a physical attack for the time being. In the future, more move types will be supported.
                try:
                    val = int(pokemonMoves[randomMove][2])
                except ValueError:
                    print("Error: Move did not pass attack check! Generating new one...")
                    continue
                break
        moveNum.Name = moveEntryToName(pokemonMoves[randomMove][0])
        moveNum.EntryNumber = randomMove #Used to find the entry from the dataset again
        moveNum.Type = convert_num_to_type(pokemonMoves[randomMove][1])
        moveNum.Power = pokemonMoves[randomMove][2]
        moveNum.PPTotal = pokemonMoves[randomMove][3]
        moveNum.PPCurrent = moveNum.PPTotal
        moveNum.Accuracy = pokemonMoves[randomMove][4]
        if pokemonMoves[randomMove][5] == "":
            print('Move has no priority value! Assigning default.')
            moveNum.Priority = 0
        else:
            moveNum.Priority = pokemonMoves[randomMove][5]

    def takeDamage(self, enemyPokemon, usedMove): #return 1 if super effective
        temp = self.CurrentHP
        typeMultiplyer = getTypeEffectiveness(convert_type_to_num(usedMove.Type), convert_type_to_num(enemyPokemon.TypeOne))
        self.CurrentHP = int(self.CurrentHP - ((((((2*enemyPokemon.Level)/5)+2*usedMove.Power*(enemyPokemon.Attack/self.Defense))/50)+2)*3*typeMultiplyer))
        if self.CurrentHP < 0:
            self.CurrentHP = 0
        temp = temp - self.CurrentHP
        print(f'Dealt {temp} damage to {enemyPokemon.Name} using {usedMove.Name}.')
        if typeMultiplyer == 0.5: #Not effective
            return 2
        if typeMultiplyer == 2: #Super effective
            return 1
    
    def numericalInputToMove(self, moveNum): #converts integer to move number
        if moveNum == 1:
            return self.MoveOne
        elif moveNum == 2:
            return self.MoveTwo
        elif moveNum == 3:
            return self.MoveThree
        elif moveNum == 4:
            return self.MoveFour
        else:
            return ""

#Discord Bot Commands
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(" ")

@client.event
async def on_message(message):
    #Bot Message Functions
    def check(reaction, user):
            return not user.bot #user == message.author
    
    #Displays a multiplayer user interface to get the players on each side
    async def multiplayerGame():
        Player1 = None
        Player2 = None
        while(1):
            menu = await message.channel.send(f'Starting a new multiplayer game! Please select either {wordToEmoji("red")} or {wordToEmoji("blue")} to pick a side!\n{wordToEmoji("red")} **Player 1 -** {Player1}\n{wordToEmoji("blue")} **Player 2 -** {Player2}')
            if(Player1 != None and Player2 != None):
                menu2 = await message.channel.send('Ready to start?')
                await menu2.add_reaction(wordToEmoji('check'))
                await menu2.add_reaction(wordToEmoji('x'))
                while (1):
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check) #wait for user to react
                    except asyncio.TimeoutError:
                        await menu.delete()
                        await menu2.delete()
                        return "", ""
                    print("reaction detected!")
                    if reaction.emoji != wordToEmoji('check') and reaction.emoji != wordToEmoji('x'): #fixes a bug where the bot responds to any emoji reaction
                        continue
                    else:
                        break
                if(reaction.emoji == wordToEmoji('check')):
                    await menu.delete()
                    await menu2.delete()
                    return Player1, Player2
                elif(reaction.emoji == wordToEmoji('x')):
                    await menu.delete()
                    await menu2.delete()
                    return "", ""
                    break
            await menu.add_reaction(wordToEmoji('red'))
            await menu.add_reaction(wordToEmoji('blue'))
            while (1):
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check) #wait for user to react
                except asyncio.TimeoutError:
                    await menu.delete()
                    return "", ""
                if reaction.emoji != wordToEmoji('red') and reaction.emoji != wordToEmoji('blue'): #fixes a bug where the bot responds to any emoji reaction
                    continue
                else:
                    break
            if(reaction.emoji == wordToEmoji('red')):
                if(Player1 == user):
                    Player1 = None
                else:
                    Player1 = user
            elif(reaction.emoji == wordToEmoji('blue')):
                if(Player2 == user):
                    Player2 = None
                else:
                    Player2 = user
            await menu.delete()

    #displays the user input and gets a players move decision
    #0 = ran from battle 1-4 = a move number
    async def playerInput(userPokemon, location):
        while (1):
            menu = await location.send(f'What will {userPokemon.Name} do?\n{wordToEmoji("red")} - Attack\n{wordToEmoji("blue")} - Run')
            await menu.add_reaction(wordToEmoji('red'))
            await menu.add_reaction(wordToEmoji('blue'))
            while (1):
                print('Users turn. Waiting for menu seleciton.')
                try: 
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check) #wait for user to react
                except asyncio.TimeoutError:
                    await menu.delete()
                    return ""
                if reaction.emoji != wordToEmoji('red') and reaction.emoji != wordToEmoji('blue'): #fixes a bug where the bot responds to any emoji reaction
                    continue
                else:
                    break
            #Display attack options
            if reaction.emoji == wordToEmoji('red'):
                await menu.delete()
                menu = await location.send(f'Attack:\n{wordToEmoji("red")} - **[{userPokemon.MoveOne.Type}]** {userPokemon.MoveOne.Name}\n{wordToEmoji("blue")} - **[{userPokemon.MoveTwo.Type}]** {userPokemon.MoveTwo.Name}\n{wordToEmoji("yellow")} - **[{userPokemon.MoveThree.Type}]** {userPokemon.MoveThree.Name}\n{wordToEmoji("green")} - **[{userPokemon.MoveFour.Type}]** {userPokemon.MoveFour.Name}')
                await menu.add_reaction(wordToEmoji('back'))
                await menu.add_reaction(wordToEmoji('red'))
                await menu.add_reaction(wordToEmoji('blue'))
                await menu.add_reaction(wordToEmoji('yellow'))
                await menu.add_reaction(wordToEmoji('green'))
                while (1):
                    print('Users turn. Waiting for menu seleciton.')
                    try: 
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check) #wait for user to react
                    except asyncio.TimeoutError:
                        await menu.delete()
                        return ""
                    if reaction.emoji != wordToEmoji('back') and reaction.emoji != wordToEmoji('red') and reaction.emoji != wordToEmoji('blue') and reaction.emoji != wordToEmoji('yellow') and reaction.emoji != wordToEmoji('green'): #fixes a bug where the bot responds to any emoji reaction
                        continue
                    else:
                        break
                if reaction.emoji == wordToEmoji('back'):
                    await menu.delete()
                    continue
                #attack cases
                elif reaction.emoji == wordToEmoji('red'):
                    await menu.delete()
                    return 1
                elif reaction.emoji == wordToEmoji('blue'):
                    await menu.delete()
                    return 2
                elif reaction.emoji == wordToEmoji('yellow'):
                    await menu.delete()
                    return 3
                elif reaction.emoji == wordToEmoji('green'):
                    await menu.delete()
                    return 4
                else:
                    print("PLAYER INPUT: Could not read decision. This is a bug!")
            #run menu option
            elif reaction.emoji == wordToEmoji('blue'):
                await menu.delete()
                return 0 #Battle ends
            else: #This happens if the user is idle and does not select anything.
                return ""
    
    def runMoveSelection(userPokemon, userMoveSelection, enemyPokemon, enemyMoveSelection):
        userMove = userPokemon.numericalInputToMove(userMoveSelection)
        enemyMove = enemyPokemon.numericalInputToMove(enemyMoveSelection)
        global discordOutput

        def performUserMove():
            global discordOutput
            discordOutput = discordOutput + f'{userPokemon.Name} used {userMove.Name}!\n'
            dealDamage = enemyPokemon.takeDamage(userPokemon, userMove)
            if dealDamage == 1: #super effective if function returns 1
                discordOutput = discordOutput + 'Its super effective!\n'
            if dealDamage == 2: #not effective if function returns 2
                discordOutput = discordOutput + 'Its not very effective...\n'
        def performEnemyMove():
            global discordOutput
            discordOutput = discordOutput + f'The opposing {enemyPokemon.Name} used {enemyMove.Name}!\n'
            dealDamage = userPokemon.takeDamage(enemyPokemon, enemyMove)
            if dealDamage == 1: #super effective if function returns 1
                discordOutput = discordOutput + 'Its super effective!\n'
            if dealDamage == 2: #not effective if function returns 2
                discordOutput = discordOutput + 'Its not very effective...\n'

        if userMove == "":
            print(userMove)
            return ""

        if userMove.Priority > enemyMove.Priority: #User attacks first
            performUserMove()
            if enemyPokemon.CurrentHP == 0:
                discordOutput = discordOutput + f'{enemyPokemon.Name} has fainted.\n'
                return 0
            performEnemyMove()
            if userPokemon.CurrentHP == 0:
                discordOutput = discordOutput + f'{userPokemon.Name} has fainted.\n'
                return 1
        elif userMove.Priority < enemyMove.Priority: #Enemy attacks first
            performEnemyMove()
            if userPokemon.CurrentHP == 0:
                discordOutput = discordOutput + f'{userPokemon.Name} has fainted.\n'
                return 1
            performUserMove()
            if enemyPokemon.CurrentHP == 0:
                discordOutput = discordOutput + f'{enemyPokemon.Name} has fainted.\n'
                return 0
        elif userMove.Priority == enemyMove.Priority and userPokemon.Speed > enemyPokemon.Speed: #User attacks first
            performUserMove()
            if enemyPokemon.CurrentHP == 0:
                discordOutput = discordOutput + f'{enemyPokemon.Name} has fainted.\n'
                return 0
            performEnemyMove()
            if userPokemon.CurrentHP == 0:
                discordOutput = discordOutput + f'{userPokemon.Name} has fainted.\n'
                return 1
        elif userMove.Priority == enemyMove.Priority and userPokemon.Speed < enemyPokemon.Speed: #Enemy attacks first
            performEnemyMove()
            if userPokemon.CurrentHP == 0:
                discordOutput = discordOutput + f'{userPokemon.Name} has fainted.\n'
                return 1
            performUserMove()
            if enemyPokemon.CurrentHP == 0:
                discordOutput = discordOutput + f'{enemyPokemon.Name} has fainted.\n'
                return 0
        else:
            print('RUN MOVE SELECTION: Nothing Happened... This is a bug!')

    if message.author == client.user:
        return

    global discordOutput

    if message.content.startswith('!pkmn'): 
        #Random encounter battle loop
        if message.content.startswith('!pkmn wEncounter'):
            #battle initial setup
            isInBattle = 1
            baseLevel = random.randint(3, 98) #level is generated between 3 and 98 because the real range is baseLevel +- up to 2
            userPokemon = Pokemon()
            enemyPokemon = Pokemon()
            userPokemon.selectNewPokemon(baseLevel)
            enemyPokemon.selectNewPokemon(baseLevel)
            combatContext = await message.channel.send(f"Running through the tall grass...\nA wild {enemyPokemon.Name} has appeared!\nGo {userPokemon.Name}!\n**                                                                       {enemyPokemon.Name} [HP: {enemyPokemon.CurrentHP}/{enemyPokemon.TotalHP} | Lvl: {enemyPokemon.Level}]\n[HP: {userPokemon.CurrentHP}/{userPokemon.TotalHP} | Lvl: {userPokemon.Level}] {userPokemon.Name}**")
            #main battle loop
            while isInBattle:
                discordOutput = "" #All info the bot needs to send to discord should be stored in this variable
                playerDecision = await playerInput(userPokemon, message.channel)
                if playerDecision == 0:
                    isInBattle = 0
                    await message.channel.send('You got away safely.')
                    print('Battle has ended!')
                    break
                randomEnemyMove = random.randint(1, 4) #Randomly decides on a move for the enemy to use
                result = runMoveSelection(userPokemon, playerDecision, enemyPokemon, randomEnemyMove)
                status = f"**                                                                       {enemyPokemon.Name} [HP: {enemyPokemon.CurrentHP}/{enemyPokemon.TotalHP} | Lvl: {enemyPokemon.Level}]\n[HP: {userPokemon.CurrentHP}/{userPokemon.TotalHP} | Lvl: {userPokemon.Level}] {userPokemon.Name}**"
                discordOutput = discordOutput + status
                await combatContext.delete()
                if result == "":
                    discordOutput = discordOutput + '\nUser was idle for too long! Battle has ended.'
                    await message.channel.send(discordOutput)
                    isInBattle = 0
                    print('Battle has ended!')
                    break
                if result == 0:
                    discordOutput = discordOutput + '\nYou Win!'
                    await message.channel.send(discordOutput)
                    isInBattle = 0
                    print('Battle has ended!')
                    break
                if result == 1:
                    discordOutput = discordOutput + '\nTry Again?'
                    await message.channel.send(discordOutput)
                    isInBattle = 0
                    print('Battle has ended!')
                    break
                combatContext = await message.channel.send(discordOutput)
                continue

        #Beta Multiplayer Battles
        elif message.content.startswith('!pkmn pBattle'):
            while(1):
                #battle initial setup
                Player1 = None
                Player2 = None
                Player1, Player2 = await multiplayerGame()
                if(Player1 == "" and Player2 == ""):
                    await message.channel.send('Game setup has been terminated.')
                    break
                isInBattle = 1
                baseLevel = random.randint(3, 98) #level is generated between 3 and 98 because the real range is baseLevel +- up to 2
                player1Pokemon = Pokemon()
                player2Pokemon = Pokemon()
                player1Pokemon.selectNewPokemon(baseLevel)
                player2Pokemon.selectNewPokemon(baseLevel)
                combatContext = await message.channel.send(f"{Player1} has challenged {Player2} to a Pokemon battle!\n{Player1} sends out {player1Pokemon.Name} and {Player2} sends out {player2Pokemon.Name}!\n**                                                                       {player2Pokemon.Name} [HP: {player2Pokemon.CurrentHP}/{player2Pokemon.TotalHP} | Lvl: {player2Pokemon.Level}]\n[HP: {player1Pokemon.CurrentHP}/{player1Pokemon.TotalHP} | Lvl: {player1Pokemon.Level}] {player1Pokemon.Name}**")
                #main battle loop
                #The main loop for multiplayer requires quite a bit of work
                #Discord can check the reactions of messages in a server but not through DMs
                #This is not ideal but the current solution is to have it send both player inputs to the server
                while isInBattle:
                    discordOutput = "" #All info the bot needs to send to discord should be stored in this variable
                    #Get player 1 input
                    p2message = await message.channel.send(f"It's {Player1}'s turn!") #change to Player2.send later
                    while(1):
                        #p1message = await Player1.send("It's your turn!")
                        player1Decision = await playerInput(player1Pokemon, message.channel) #Change to Player1 in the future
                        if player1Decision == 0:
                            runMessage = await message.channel.send("You cannot run from a player battle!") #change to Player1.send later
                            continue
                        #await p1message.delete()
                        await p2message.delete()
                        await runMessage.delete()
                        break
                    #Get player 2 input
                    p1message = await message.channel.send(f"It's {Player2}'s turn!") #change to Player1.send later
                    while(1):
                        #p2message = await Player2.send("It's your turn!")
                        player2Decision = await playerInput(player2Pokemon, message.channel) #Change to Player2 in the future
                        if player2Decision == 0:
                            runMessage = await message.channel.send("You cannot run from a player battle!") #change to Player2.send later
                            continue
                        await p1message.delete()
                        #await p2message.delete()
                        runMessage.delete()
                        break
                    result = runMoveSelection(player1Pokemon, player1Decision, player2Pokemon, player2Decision)
                    status = f"**                                                                       {player2Pokemon.Name} [HP: {player2Pokemon.CurrentHP}/{player2Pokemon.TotalHP} | Lvl: {player2Pokemon.Level}]\n[HP: {player1Pokemon.CurrentHP}/{player1Pokemon.TotalHP} | Lvl: {player1Pokemon.Level}] {player1Pokemon.Name}**"
                    discordOutput = discordOutput + status
                    await combatContext.delete()
                    if result == "":
                        discordOutput = discordOutput + '\nUser was idle for too long! Battle has ended.'
                        await message.channel.send(discordOutput)
                        isInBattle = 0
                        print('Battle has ended!')
                        break
                    if result == 0:
                        discordOutput = discordOutput + f'\n{Player2} Wins!'
                        await message.channel.send(discordOutput)
                        isInBattle = 0
                        print('Battle has ended!')
                        break
                    if result == 1:
                        discordOutput = discordOutput + f'\n{Player1} Wins!'
                        await message.channel.send(discordOutput)
                        isInBattle = 0
                        print('Battle has ended!')
                        break
                    combatContext = await message.channel.send(discordOutput)
                    continue
                break

        #Run auto update system
        elif message.content.startswith('!pkmn Update'):
            await message.channel.send('Updating from source and restarting...') 
            global runProgramUpdate
            runProgramUpdate = 1
            await client.close()

        #Default response when a command is not detected
        else:
            await message.channel.send('Unrecognized command! The available options are:\n\n wEncounter --Start a fully randomized Wild Pokemon Encounter\n pBattle --Start a fully randomized PvP battle\n Update --Update bot from source and restart') #\n- lookup --Pull up the data entry for a given Pokemon

client.run(botToken) #Discord bot token. Now applied externally via botToken.txt