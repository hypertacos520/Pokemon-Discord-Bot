#DISCLAIMER: Tons of bugs should be expected as well as things that don't make any sense.

#Import Libraries
import discord
import random
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

#Define Classes
class pokemonMove:
    Name = None
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
        self.Name = pokemonData[pokemonEntryNumber][0]
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
        moveNum.Name = pokemonMoves[randomMove][0]
        moveNum.Type = convert_num_to_type(pokemonMoves[randomMove][1])
        moveNum.Power = pokemonMoves[randomMove][2]
        moveNum.PP = pokemonMoves[randomMove][3]
        moveNum.Accuracy = pokemonMoves[randomMove][4]
        moveNum.Priority = pokemonMoves[randomMove][5]

    def takeDamage(self, enemyPokemon, usedMove): #return 1 if super effective
        temp = self.CurrentHP
        self.CurrentHP = int(self.CurrentHP - (((((2*enemyPokemon.Level)/5)+2*usedMove.Power*(enemyPokemon.Attack/self.Defense))/50)+2)*3)
        if self.CurrentHP < 0:
            self.CurrentHP = 0
        temp = temp - self.CurrentHP
        print(f'Dealt {temp} damage.')

#Discord Bot Commands
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(" ")

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('!pkmn'):
        def check(reaction, user):
            return user == message.author 

        #Random encounter battle loop
        if message.content.startswith('!pkmn wBattle'):
            #battle initial setup
            isInBattle = 1
            baseLevel = random.randint(4, 97) #level is generated between 4 and 97 because the real range is baseLevel +- up to 2
            userPokemon = Pokemon()
            enemyPokemon = Pokemon()
            userPokemon.selectNewPokemon(baseLevel)
            enemyPokemon.selectNewPokemon(baseLevel)
            await message.channel.send(f"Running through the tall grass...\nA wild {enemyPokemon.Name} has appeared!\nGo {userPokemon.Name}!")
            #main battle loop
            while isInBattle:
                status = await message.channel.send(f"**                                                                       {enemyPokemon.Name} [HP: {enemyPokemon.CurrentHP}/{enemyPokemon.TotalHP} | Lvl: {enemyPokemon.Level}]\n[HP: {userPokemon.CurrentHP}/{userPokemon.TotalHP} | Lvl: {userPokemon.Level}] {userPokemon.Name}**") 
                if enemyPokemon.CurrentHP == 0:
                    await message.channel.send(f'{enemyPokemon.Name} has fainted.\nYou win!')
                    isInBattle = 0
                    break
                if userPokemon.CurrentHP == 0:
                    await message.channel.send(f'{userPokemon.Name} has fainted.\nTry again?')
                    isInBattle = 0
                    break
                msg = await message.channel.send(f'What will {userPokemon.Name} do?\n🔴 - Attack\n🔵 - Run')
                await msg.add_reaction('🔴')
                await msg.add_reaction('🔵')
                while (1):
                    print('Users turn. Waiting for menu seleciton.')
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check) #wait for user to react
                    if reaction.emoji != '🔴' and reaction.emoji != '🔵':
                        continue
                    else:
                        break
                #show attack menu
                if reaction.emoji == '🔴':
                    print('User reacted with 🔴. Displaying attack menu.')
                    await msg.delete()
                    msg = await message.channel.send(f'Attack:\n🔴 - [{userPokemon.MoveOne.Type}] {userPokemon.MoveOne.Name}\n🔵 - [{userPokemon.MoveTwo.Type}] {userPokemon.MoveTwo.Name}\n🟡 - [{userPokemon.MoveThree.Type}] {userPokemon.MoveThree.Name}\n🟢 - [{userPokemon.MoveFour.Type}] {userPokemon.MoveFour.Name}')
                    await msg.add_reaction('⬅')
                    await msg.add_reaction('🔴')
                    await msg.add_reaction('🔵')
                    await msg.add_reaction('🟡')
                    await msg.add_reaction('🟢')
                    while (1):
                        print('Users turn. Waiting for menu seleciton.')
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check) #wait for user to react
                        if reaction.emoji != '⬅' and reaction.emoji != '🔴' and reaction.emoji != '🔵' and reaction.emoji != '🟡' and reaction.emoji != '🟢':
                            continue
                        else:
                            break
                    if reaction.emoji == '⬅':
                        print('User reacted with ⬅. Returning to previous menu.')
                        await status.delete()
                        await msg.delete()
                        continue
                    #attack cases
                    elif reaction.emoji == '🔴':
                        print(f'User reacted with 🔴. Using {userPokemon.MoveOne.Name}.')
                        await msg.delete()
                        await message.channel.send(f'{userPokemon.Name} used {userPokemon.MoveOne.Name}!')
                        dealDamage = enemyPokemon.takeDamage(userPokemon, userPokemon.MoveOne)
                        if dealDamage == 1: #super effective if function returns 1
                            await message.channel.send('Its super effective!')
                    elif reaction.emoji == '🔵':
                        print(f'User reacted with 🔵. Using {userPokemon.MoveTwo.Name}.')
                        await msg.delete()
                        await message.channel.send(f'{userPokemon.Name} used {userPokemon.MoveTwo.Name}!')
                        dealDamage = enemyPokemon.takeDamage(userPokemon, userPokemon.MoveTwo)
                        if dealDamage == 1: #super effective if function returns 1
                            await message.channel.send('Its super effective!')
                    elif reaction.emoji == '🟡':
                        print(f'User reacted with 🟡. Using {userPokemon.MoveThree.Name}.')
                        await msg.delete()
                        await message.channel.send(f'{userPokemon.Name} used {userPokemon.MoveThree.Name}!')
                        dealDamage = enemyPokemon.takeDamage(userPokemon, userPokemon.MoveThree)
                        if dealDamage == 1: #super effective if function returns 1
                            await message.channel.send('Its super effective!')
                    elif reaction.emoji == '🟢':
                        print(f'User reacted with 🟢. Using {userPokemon.MoveFour.Name}.')
                        await msg.delete()
                        await message.channel.send(f'{userPokemon.Name} used {userPokemon.MoveFour.Name}!')
                        dealDamage = enemyPokemon.takeDamage(userPokemon, userPokemon.MoveFour)
                        if dealDamage == 1: #super effective if function returns 1
                            await message.channel.send('Its super effective!')
                    randomMove = random.randrange(4)
                    if randomMove == 0:
                        await message.channel.send(f'The opposing {enemyPokemon.Name} used {enemyPokemon.MoveOne.Name}!')
                        dealDamage = userPokemon.takeDamage(enemyPokemon, enemyPokemon.MoveOne)
                        if dealDamage == 1: #super effective if function returns 1
                                await message.channel.send('Its super effective!')
                    elif randomMove == 1:
                        await message.channel.send(f'The opposing {enemyPokemon.Name} used {enemyPokemon.MoveTwo.Name}!')
                        dealDamage = userPokemon.takeDamage(enemyPokemon, enemyPokemon.MoveTwo)
                        if dealDamage == 1: #super effective if function returns 1
                                await message.channel.send('Its super effective!')
                    elif randomMove == 2:
                        await message.channel.send(f'The opposing {enemyPokemon.Name} used {enemyPokemon.MoveThree.Name}!')
                        dealDamage = userPokemon.takeDamage(enemyPokemon, enemyPokemon.MoveThree)
                        if dealDamage == 1: #super effective if function returns 1
                                await message.channel.send('Its super effective!')
                    elif randomMove == 3:
                        await message.channel.send(f'The opposing {enemyPokemon.Name} used {enemyPokemon.MoveFour.Name}!')
                        dealDamage = userPokemon.takeDamage(enemyPokemon, enemyPokemon.MoveFour)
                        if dealDamage == 1: #super effective if function returns 1
                                await message.channel.send('Its super effective!')
                    await status.delete()
                    continue #continues the battle loop
                #run menu option
                elif reaction.emoji == '🔵':
                    print('User reacted with 🔵. Time to run!')
                    await msg.delete()
                    await message.channel.send('You got away safely.')
                    isInBattle = 0 #Battle ends
                isInBattle = 0 #Failsafe

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