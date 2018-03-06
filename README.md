# miniBot
Minimal Python chatbot server with associated client web interface
To use as a template for chatbot projects

## Origin and aims of the project
### Affiliation
This work is carried out by the CRI Labs at the Centre for Research and Interdisciplinarity, Département Frontières du vivant et de l'apprendre, IIFR, Université Paris Descartes, Université Sorbonne Paris Cité, Paris, France.
It is funded through the French PIA IDEFI grant (ANR11 IDEFI 0023, Institut Innovant de Formation par la Recherche).
### Why a chatbot?
Chatbots are computer-driven dialog systems that mimic human conversation in natural language, either through textual or audio interaction.\
While they have long been present in the collective imagination of future technologies -in particular as talkative robots- their use has recently grown more common and they are apparently [here to stay](https://blog.ubisend.com/optimise-chatbots/chatbot-statistics). This can be explained by several factors:
* Research on natural language processing has been progressing nicely in the last decades -[for example](http://onlinelibrary.wiley.com/doi/10.1002/aris.1440370103/full)-
* Easy-to-use APIs and platforms to build your own chatbot without programming knowledge are proliferating
* Messenging apps are replacing websites and social networks for information and communication, making chatbots a relevant type of interfaces to provide services

The moment we brought up the possibility of chatbots at the CRI, many people came forward to enquire about what a chatbot could bring to their project. Of course, a chatbot interface was not suitable for all of them but there was still enough need for us to start creating this template.
### List of CRI projects scheduled to evolve from this template
* Participative research on teachers' professional and personal care and development
* Maieutic questionning app on lifelong learning for a Lifelong Learning Festival in France
* Help companion and data gathering tool in a mobile game on antibiotic resistance of tuberculosis
* Interactive FAQ for members of the CRI
### Specific goal of this template
We were not satisfied with the level of flexibility offered by free develop-your-own-chatbot APIs and platforms. They might be suitable to develop a costumer service first-responder or a commercial gateway but they are not enough for some of the atypical use cases we are hoping to create.

The goal of this repository is to build a template chatbot that can easily be replicated and trained with new content. For this we are developping three components:
* A minimalist web client interface that can be used to test the behaviour of the chatbot and modify the training content
* A server that hosts the natural language processing core, receives requests, forward them to this core, send back the core's answer and logs the exchange
* A natural language processing module that trains on provided content and can then provide a suitable answer to new requests

## Current state

## To use the chatbot
### Chat with the bot

### Change the training data for the bot

## To create a new chatbot from the template
### Questions to ask yourself before creating your chatbot

### Set up
__Warning__: Tested on Unbuntu only for now

#### Set up your environment
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

#### Set up your chatbot on your server
..*Move to the miniBot/server directory in command line
..*Run *$python server.py*
..*Wait until the model training is over and the console output a *Running on...* message
..*Ctrl^C to abort the script
..*Run *$python server.py* again
..*Your server is running and ready to accept queries!
..*Find your server public ip address if you do not already know it

#### Set up your client interface
..*Open minibot/javascript/talkToMinibot.js in a text editor
..*On line 24, replace *167.114.255.133* with your server's ip address
..*Save and close
..*Create a symbolic link from /minibot/html to /minibot/javascript and to /minibot/style (the method depends on your OS)
..*Open http://localhost/miniBot/ in your browser
..*Talk with your chatbot!

### Costumise the content
The code for the chatbot was taken from https://chatbotsmagazine.com/contextual-chat-bots-with-tensorflow-4391749d0077
You can change your chatbot's detected intents and possible answers in /minibot/server/model/intents.json

