from flask import Flask, jsonify, request
from flask_cors import CORS
'''
# Set MODEL
from model.trainBot import createModel
import model.queryBot
createModel()
'''

app = Flask(__name__)
CORS(app) # Enable queries from different domains

@app.route("/minibot/api/msg", methods=['GET', 'POST'])
def get_msg():
	data = request.form.get("msg")

	return jsonify({"msg": data})

if __name__ == "__main__":
	app.run("0.0.0.0", 8888)
