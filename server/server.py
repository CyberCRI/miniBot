from flask import Flask, jsonify, request
from flask_cors import CORS
import os.path
import sys

# Set MODEL
# Set paths for imports
appPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.getcwd())
# If not already created, create model and train it
import model.minibot

# Create the Flask app that will deal with communication and asynchrony
app = Flask(__name__)
CORS(app) # Enable queries from different domains

# Create route for bot queries
@app.route("/minibot/api/msg", methods=['GET', 'POST'])
def get_msg():
	# Receive message
	data = request.form.get("msg")
	# Process it and get answer from bot
	response = model.minibot.response(data)
	# Send answer
	return jsonify({"msg": response})

@app.route("/minibot/api/intents", methods=["GET", "POST"])
def get_intents():
	intentsPath = os.path.join(appPath, "model/intents.json")
	with open(intentsPath) as json_data:
	    intents = json.load(json_data)
	return intents

# Run app
if __name__ == "__main__":
	app.run("0.0.0.0", 8888) # 0.0.0.0 to enable external access
