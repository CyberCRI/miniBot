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

# Create route for bot queries
@app.route("/minibot/api/msg", methods=['GET', 'POST'])
def get_msg():
	# Receive message
	clientIP = request.remote_addr
	data = request.form.get("msg")
	# Process it and get answer from bot
	response = model.minibot.response(data)
	# Send answer
	logchat.createMsgLog(clientIP, "minibot", data, response)
	return jsonify({"msg": response})

@app.route("/minibot/api/intents", methods=["GET", "POST"])
def get_intents():
	# Load json data
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	# Send all data
	return jsonify(intents)

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
