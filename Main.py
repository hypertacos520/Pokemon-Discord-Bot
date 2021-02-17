#NOTE this application REQUIRES executable permissions. It needs to be able to run itself after an update is fetched.

import os
import sys
import urllib.request

botSource = "https://raw.githubusercontent.com/hypertacos520/Pokemon-Discord-Bot/master/Bot.py" #Bot itself
updaterSource = "https://raw.githubusercontent.com/hypertacos520/Pokemon-Discord-Bot/master/Main.py" #This file
currentDirectory = os.path.dirname(os.path.realpath(__file__))

def updateFile(url, fileName):
    print(f'Currently downloading {url}...')
    filename, headers = urllib.request.urlretrieve(url, filename = currentDirectory + f"/{fileName}")
    print(f'Update has successfully been downloaded to "{filename}"!')

print("Hi! I'm the management script. Let me run the bot for you...")
import Bot #We're gonna run the bot as a subprocess to the updater
if Bot.runProgramUpdate == 1:
    updateFile(botSource, "Bot.py")
    updateFile(updaterSource, "Main.py")
    print(f'Updates completed! Rebooting bot...')
    os.execv('/usr/bin/python3', ["\"" + '/usr/bin/python3' + "\""] + sys.argv) #Python path needed to be hard coded due to some issues with how the system changes the executable path
else:
    print('Bot process has terminated without requesting an update. Shutting down...')