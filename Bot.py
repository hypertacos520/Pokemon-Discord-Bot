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
pokemonData = pokemonDataSet[['Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Type 1', 'Type 2']].values.tolist()
pokemonMoves = pokemonMovesDataSet[['identifier', 'type_id', 'power', 'pp', 'accuracy', 'priority', 'damage_class_id']].values.tolist()

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
    else:
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
    PP = None
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
        moveNum.PP = pokemonMoves[randomMove][3]
        moveNum.Accuracy = pokemonMoves[randomMove][4]
        if pokemonMoves[randomMove][5] == "":
            print('Move has no priority value! Assigning default.')
            moveNum.Priority = 0
        else:
            moveNum.Priority = pokemonMoves[randomMove][5]

    def takeDamage(self, enemyPokemon, usedMove): #return 1 if super effective
        temp = self.CurrentHP
        self.CurrentHP = int(self.CurrentHP - (((((2*enemyPokemon.Level)/5)+2*usedMove.Power*(enemyPokemon.Attack/self.Defense))/50)+2)*3)
        if self.CurrentHP < 0:
            self.CurrentHP = 0
        temp = temp - self.CurrentHP
        print(f'Dealt {temp} damage to {enemyPokemon.Name} using {usedMove.Name}.')
    
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
            return None

#Discord Bot Commands
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(" ")

@client.event
async def on_message(message):
    #Bot Message Functions
    def check(reaction, user):
            return user == message.author
    
    #displays the user input and gets a players move decision
    #0 = ran from battle 1-4 = a move number
    async def playerInput(userPokemon):
        while (1):
            menu = await message.channel.send(f'What will {userPokemon.Name} do?\n{wordToEmoji("red")} - Attack\n{wordToEmoji("blue")} - Run')
            await menu.add_reaction(wordToEmoji('red'))
            await menu.add_reaction(wordToEmoji('blue'))
            while (1):
                print('Users turn. Waiting for menu seleciton.')
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check) #wait for user to react
                except asyncio.TimeoutError:
                    await menu.delete()
                    return None
                if reaction.emoji != wordToEmoji('red') and reaction.emoji != wordToEmoji('blue'): #fixes a bug where the bot responds to any emoji reaction
                    continue
                else:
                    break
            #Display attack options
            if reaction.emoji == wordToEmoji('red'):
                await menu.delete()
                menu = await message.channel.send(f'Attack:\n{wordToEmoji("red")} - [{userPokemon.MoveOne.Type}] {userPokemon.MoveOne.Name}\n{wordToEmoji("blue")} - [{userPokemon.MoveTwo.Type}] {userPokemon.MoveTwo.Name}\n{wordToEmoji("yellow")} - [{userPokemon.MoveThree.Type}] {userPokemon.MoveThree.Name}\n{wordToEmoji("green")} - [{userPokemon.MoveFour.Type}] {userPokemon.MoveFour.Name}')
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
                        return None
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
                await message.channel.send('You got away safely.')
                return 0 #Battle ends
            else: #This happens if the user is idle and does not select anything.
                return None
    
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
        def performEnemyMove():
            global discordOutput
            discordOutput = discordOutput + f'The opposing {enemyPokemon.Name} used {enemyMove.Name}!\n'
            dealDamage = userPokemon.takeDamage(enemyPokemon, enemyMove)
            if dealDamage == 1: #super effective if function returns 1
                discordOutput = discordOutput + 'Its super effective!\n'

        if userMove == None:
            return None

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

    if message.content.startswith('!pkmn'): 
        #Random encounter battle loop
        if message.content.startswith('!pkmn wBattle'):
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
                global discordOutput
                discordOutput = "" #All info the bot needs to send to discord should be stored in this variable
                playerDecision = await playerInput(userPokemon)
                if playerDecision == 0:
                    isInBattle = 0
                    print('Battle has ended!')
                    break
                randomEnemyMove = random.randint(1, 4) #Randomly decides on a move for the enemy to use
                result = runMoveSelection(userPokemon, playerDecision, enemyPokemon, randomEnemyMove)
                status = f"**                                                                       {enemyPokemon.Name} [HP: {enemyPokemon.CurrentHP}/{enemyPokemon.TotalHP} | Lvl: {enemyPokemon.Level}]\n[HP: {userPokemon.CurrentHP}/{userPokemon.TotalHP} | Lvl: {userPokemon.Level}] {userPokemon.Name}**"
                discordOutput = discordOutput + status
                await combatContext.delete()
                if result == None:
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

        #Run auto update system
        elif message.content.startswith('!pkmn Update'):
            await message.channel.send('Updating from source and restarting...') 
            global runProgramUpdate
            runProgramUpdate = 1
            await client.close()

        #Default response when a command is not detected
        else:
            await message.channel.send('You need to specify a command! The available options are:\n\n wBattle --Start a fully randomized Wild Pokemon Encounter\n Update --Update bot from source and restart') #\n- lookup --Pull up the data entry for a given Pokemon

client.run(botToken) #Discord bot token. Now applied externally via botToken.txt