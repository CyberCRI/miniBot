from flask import Flask, jsonify, request
from flask_cors import CORS
import os.path
import sys
import json
import logging
import datetime

# Set MODEL
# Set paths for imports
appPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.getcwd())
# If not already created, create model and train it
import model.minibot

# Create the Flask app that will deal with communication and asynchrony
app = Flask(__name__)
CORS(app) # Enable queries from different domains

# Set up logging
import logchat
lastLogId = {}

# Create route for bot queries
@app.route("/minibot/api/msg", methods=['GET', 'POST'])
def get_msg():
	# Receive message
	clientIP = request.remote_addr
	data = request.form.get("msg")
	# Process it and get answer from bot
	(intent, response) = model.minibot.response(data)
	# Log message exchange
	logId = logchat.createMsgLog(clientIP, "minibot", data, intent, response)
	lastLogId[clientIP] = logId
	# Send answer
	return jsonify({"msg": response})

# Create route to register improper bot response
@app.route("/minibot/api/complain", methods=["GET", "POST"])
def complainAboutAnswer():
	# Get user id
	clientIP = request.remote_addr
	# If this user already has a conversation log, issue a warning for last exchange
	try:
		logId = lastLogId[clientIP]
	except:
		print("Warning: this user is complaining but has not yet chatted with the bot.")
		return "Warning: this user is complaining but has not yet chatted with the bot."
	try:
		logchat.registerComplaint(logId)
		return "OK"
	except Exception as e:
		print(e)
		return e

# Create route for checking all intents in bot
@app.route("/minibot/api/intents", methods=["GET", "POST"])
def get_intents():
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Send all data
	return jsonify(intents)

# Create route for checking a specific intent in bot
@app.route("/minibot/api/intent", methods=["GET", "POST"])
def get_intent():
	# Receive tag for requested intents
	tag = request.form.get("tag")
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Fetch data if existing tag
	data = intents.get(tag)
	# Send data
	return jsonify(intents)

# Run app
if __name__ == "__main__":
	app.run("0.0.0.0", 8888) # 0.0.0.0 to enable external access
