from flask import Flask, jsonify, request
from flask_cors import CORS
import os.path
import sys
import json
import logging
import datetime
import importlib

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
	# Receive tag for requested intent
	tag = request.form.get("tag")
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Fetch data if existing tag
	data = {}
	for intent in intents["intents"]:
		if intent["tag"] == tag:
			data = intent
			break
	# Send data
	return jsonify(data)

# Create route for adding a pattern to a specific intent in bot
@app.route("/minibot/api/add_pattern", methods=["GET", "POST"])
def add_pattern():
	# Receive tag and pattern for requested intent
	tag = request.form.get("tag")
	pattern = request.form.get("pattern")
	clientIP = request.remote_addr
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Fetch data if existing tag
	data = {}
	for i in range(len(intents["intents"])):
		if intents["intents"][i]["tag"] == tag:
			data = intents["intents"][i]
			break
	# Check if tag existed
	if len(data) == 0:
		logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newPattern = pattern, status = "error", statusDetails = "No intent")
		return jsonify({"status": "No intent"})
	# Add pattern
	data["patterns"].append(pattern)
	# Save modification
	intents["intents"][i] = data
	with open(intentsPath, 'w') as json_file:
	    json.dump(intents, json_file)
	# Send data
	logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newPattern = pattern)
	return jsonify({"status": "Pattern added"})

# Create route for modifying a pattern of a specific intent in bot
@app.route("/minibot/api/modify_pattern", methods=["GET", "POST"])
def modify_pattern():
	# Receive tag and pattern for requested intent
	tag = request.form.get("tag")
	oldPattern = request.form.get("oldPattern")
	newPattern = request.form.get("newPattern")
	clientIP = request.remote_addr
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Fetch data if existing tag
	data = {}
	for i in range(len(intents["intents"])):
		if intents["intents"][i]["tag"] == tag:
			data = intents["intents"][i]
			break
	# Check if tag existed
	if len(data) == 0:
		logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newPattern = newPattern, oldPattern = oldPattern, status = "error", statusDetails = "No intent")
		return jsonify({"status": "No intent"})
	# Modify pattern
	try:
		data["patterns"][data["patterns"].index(oldPattern)] = newPattern
	except:
		logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newPattern = newPattern, oldPattern = oldPattern, status = "error", statusDetails = "No matching pattern")
		return jsonify({"status": "No matching pattern"})
	# Save modification
	intents["intents"][i] = data
	with open(intentsPath, 'w') as json_file:
	    json.dump(intents, json_file)
	# Send data
	logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newPattern = newPattern, oldPattern = oldPattern)
	return jsonify({"status": "Pattern modified"})

# Create route for adding a response to a specific intent in bot
@app.route("/minibot/api/add_response", methods=["GET", "POST"])
def add_response():
	# Receive tag and pattern for requested intent
	tag = request.form.get("tag")
	response = request.form.get("response")
	clientIP = request.remote_addr
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Fetch data if existing tag
	data = {}
	for i in range(len(intents["intents"])):
		if intents["intents"][i]["tag"] == tag:
			data = intents["intents"][i]
			break
	# Check if tag existed
	if len(data) == 0:
		logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newResponse = response, status = "error", statusDetails = "No intent")
		return jsonify({"status": "No intent"})
	# Add response
	data["responses"].append(response)
	# Save modification
	intents["intents"][i] = data
	with open(intentsPath, 'w') as json_file:
	    json.dump(intents, json_file)
	# Send data
	logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newResponse = response)
	return jsonify({"status": "Response added"})

# Create route for modifying a response of a specific intent in bot
@app.route("/minibot/api/modify_response", methods=["GET", "POST"])
def modify_response():
	# Receive tag and pattern for requested intent
	tag = request.form.get("tag")
	oldResponse = request.form.get("oldResponse")
	newResponse = request.form.get("newResponse")
	clientIP = request.remote_addr
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Fetch data if existing tag
	data = {}
	for i in range(len(intents["intents"])):
		if intents["intents"][i]["tag"] == tag:
			data = intents["intents"][i]
			break
	# Check if tag existed
	if len(data) == 0:
		logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newResponse = newResponse, oldResponse = oldResponse, status = "error", statusDetails = "No intent")
		return jsonify({"status": "No intent"})
	# Modify response
	try:
		data["responses"][data["responses"].index(oldResponse)] = newResponse
	except:
		logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newResponse = newResponse, oldResponse = oldResponse, status = "error", statusDetails = "No matching response")
		return jsonify({"status": "No matching response"})
	# Save modification
	intents["intents"][i] = data
	with open(intentsPath, 'w') as json_file:
	    json.dump(intents, json_file)
	# Send data
	logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, newResponse = newResponse, oldResponse = oldResponse)
	return jsonify({"status": "Response modified"})

# Create route for adding an intent in bot
@app.route("/minibot/api/add_intent", methods=["GET", "POST"])
def add_intent():
	# Receive tag and pattern for requested intent
	tag = request.form.get("tag")
	patterns = request.form.getlist("patterns[]")
	responses = request.form.getlist("responses[]")
	clientIP = request.remote_addr
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Check if tag already exists
	for i in range(len(intents["intents"])):
		if intents["intents"][i]["tag"] == tag:
			logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, patterns = patterns, responses = responses, status = "warning", statusDetails = "Cannot override existing intent")
			return jsonify({"status": "Cannot overwrite intent"})
	# Construct new intent
	data = {
		"tag": tag,
		"patterns": patterns,
		"responses": responses
	}
	# Save modification
	intents["intents"].append(data)
	with open(intentsPath, 'w') as json_file:
	    json.dump(intents, json_file)
	# Send data
	logId = logchat.createIntentsModifLog(clientIP, "minibot", tag, patterns = patterns, responses = responses)
	return jsonify({"status": "Intent added"})

# Create route for retraining bot
@app.route("/minibot/api/retrain", methods=["GET", "POST"])
def retrain():
	# Delete training data
	os.remove(os.path.join(appPath, "model/training_data"))
	importlib.reload(model.minibot)

	clientIP = request.remote_addr
	logId = logchat.registerRetrain(clientIP, "minibot")
	return jsonify({"status": "Retrained model"})


# Run app
if __name__ == "__main__":
	app.run("0.0.0.0", 8888) # 0.0.0.0 to enable external access
