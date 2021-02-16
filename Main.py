import os
import sys
import urllib.request

#NOTE this application REQUIRES executable permissions. It needs to be able to run itself after an update is fetched.
applicationSource = "https://raw.githubusercontent.com/hypertacos520/Pokemon-Discord-Bot/master/botMain.py" #Change to download link from github
currentDirectory = os.path.dirname(os.path.realpath(__file__))

print("Hi! I'm the management script. Let me run the bot for you...")
import botMain #We're gonna run the bot as a subprocess to the updater
if botMain.runProgramUpdate == 1:
    print(f'The bot has requested an update!\nUpdating from {applicationSource}...')
    #run actual file download here
    filename, headers = urllib.request.urlretrieve(applicationSource, filename = currentDirectory + "/botMain.py")
    print(f'Update has successfully been downloaded to {filename}! Rebooting bot...')
    os.execv('/usr/bin/python3', ["\"" + '/usr/bin/python3' + "\""] + sys.argv) #Python path needed to be hard coded due to some issues with how the system changes the executable path
else:
    print('Bot process has terminated without requesting an update. Shutting down...')