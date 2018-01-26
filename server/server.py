from flask import Flask, jsonify, request
from flask_cors import CORS
import os.path
import sys

# Set MODEL
# Set paths for imports
appPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.getcwd())
# If not already created, create model and train it
# WARNING: For now if creating the model, the server needs to be restarted to use it
if not os.path.isfile(os.path.join(appPath, "model/training_data")):
	from model.trainBot import createModel
	createModel()
else:
	# If model already exists, import it
	import model.queryBot


# Create the Flask app that will deal with communication and asynchrony
app = Flask(__name__)
CORS(app) # Enable queries from different domains

# Create route for bot queries
@app.route("/minibot/api/msg", methods=['GET', 'POST'])
def get_msg():
	# Receive message
	data = request.form.get("msg")
	# Process it and get answer from bot
	response = model.queryBot.response(data)
	# Send answer
	return jsonify({"msg": response})

# Run app
if __name__ == "__main__":
	app.run("0.0.0.0", 8888) # 0.0.0.0 to enable external access
