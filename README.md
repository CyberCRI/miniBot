# miniBot
Minimal Python chatbot server with associated client web interface
To use as a template for chatbot projects

## To use this project as a base for your chatbot
__Warning__: Tested on Unbuntu only for now

### Set up your environment
Clone or download this repo where you want your client and where you want your server (or only once if you plan to have both in the same location of one computer)

What you need for the server:
..*Python3
...Check that *$python* runs Python3 (run *$python -V*)
...If not and you don't need to use Python2 on that computer:
....*In your .bashrc or .bash_aliases file, add *alias python=python3*
....*run *$sudo ln -s /Library/Frameworks/Python.framework/Versions3.4/lib/python3.4/site-packages /usr/local/lib/python3.4/site-packages*
...If not and you need Python2 on this computer, I do not have the solution yet, you might have to modify some of the code
..*Python3 packages flask, flask_cors, nltk, numpy, tflearn, tensorflow, jsonschema
..*nltk data
...In command line: *sudo python3 -m nltk.downloader -d /usr/local/share/nltk_data all*
...Instructions for the interactive installer: http://www.nltk.org/data.html

What you need for the client:
..*A localhost server (I recommend installing LAMP/MAMP/WAMP)
..*If you did not clone the repo in your localhost server's source directory, create a symbolic link between them (the method depends on your OS)

### Set up your chatbot on your server
..*Move to the miniBot/server directory in command line
..*Run *$python server.py*
..*Wait until the model training is over and the console output a *Running on...* message
..*Ctrl^C to abort the script
..*Run *$python server.py* again
..*Your server is running and ready to accept queries!
..*Find your server public ip address if you do not already know it

### Set up your client interface
..*Open minibot/javascript/talkToMinibot.js in a text editor
..*On line 24, replace *167.114.255.133* with your server's ip address
..*Save and close
..*Create a symbolic link from /minibot/html to /minibot/javascript and to /minibot/style (the method depends on your OS)
..*Open http://localhost/miniBot/ in your browser
..*Talk with your chatbot!

## To modify the bot
The code for the chatbot was taken from https://chatbotsmagazine.com/contextual-chat-bots-with-tensorflow-4391749d0077
You can change your chatbot's detected intents and possible answers in /minibot/server/model/intents.json

