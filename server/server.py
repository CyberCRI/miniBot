from flask import Flask, jsonify, request
from flask_cors import CORS
import os.path
import sys

# Set MODEL
# If not already created, create model and train it
appPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.getcwd())
if not os.path.isfile(os.path.join(appPath, "model/training_data")):
	from model.trainBot import createModel
	createModel()
else:
	import model.queryBot



app = Flask(__name__)
CORS(app) # Enable queries from different domains


@app.route("/minibot/api/msg", methods=['GET', 'POST'])
def get_msg():
	data = request.form.get("msg")
	response = model.queryBot.response(data)
	return jsonify({"msg": response})

if __name__ == "__main__":
	app.run("0.0.0.0", 8888)
