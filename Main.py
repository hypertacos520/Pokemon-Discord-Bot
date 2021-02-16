from importlib import reload
applicationSource = None #Change to download link from github

print("Hi! I'm the management script. Let me run the bot for you...")
import botMain #We're gonna run the bot as a subprocess to the updater
botMain = reload(botMain)

while(1):
    if botMain.runProgramUpdate == 1:
        print('The bot has requested an update')
        print(f'Updating from {applicationSource}...')
        #run actual file download here
        print('Update has completed! Rebooting bot...')
        botMain.runProgramUpdate = 0
        continue
    else:
        print('Bot process has terminated without requesting an update. Shutting down...')
        break