import botMain.py as bot #We're gonna run the bot as a subprocess to the updater

runProgramUpdate = 0
applicationSource = None #Change to download link from github

while(1):
    runProgramUpdate = bot
    if runProgramUpdate == 1:
        print('The bot has requested an update')
        print(f'Updating from {applicationSource}...')
        #run actual file download here
        print('Update has completed! Rebooting bot...')
        continue
    else:
        print('Bot process has terminated without requesting an update. Shutting down...')
        break