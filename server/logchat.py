from jsonschema import validate
import json
from pymongo import MongoClient
import datetime

# Define a JSON schema for log entries
schema = {
    "$schema": "http://167.114.255.133:8888/minibot/api/schema#",
    "title": "Log",
    "description": "Log entry for minibot",
    "type" : "object",
    "properties" : {
        "entryType" : {
            "description": "The type of entry",
            "type" : "string",
            "enum": ["msg"]
        },
        "owner" : {
            "description" : "The identifier of the owner of the request",
            "type" : "string"
        },
        "bot" : {
            "description" : "The id of the bot associated with the request",
            "type" : "string"
        },
        "datetime" : {
            "description" : "The time of creation of this log entry",
            "type" : "string",
            "format" : "date-time"
        },
        "content" : {
            "description" : "The content of the entry",
            "type" : "object",
            "properties" : {
                "userMsg" : {
                    "description" : "The message from the user",
                    "type" : "string"
                },
                "intent" : {
                    "description" : "The intent extracted from userMsg",
                    "type" : "string"
                },
                "botMsg" : {
                    "description" : "The answer provided by the bot",
                    "type" : "string"
                }
            }
        },
        "status" : {
            "description" : "Errors and warnings",
            "type" : "object",
            "properties" : {
                "tag" : {
                    "description" : "The completion tag",
                    "type" : "string",
                    "enum" : ["success", "error", "warning"]
                },
                "details" : {
                    "description" : "Information on the error or warning",
                    "type" : "string"
                }
            }
        }
    },
    "required": ["entryType", "owner", "bot", "datetime", "content", "status"]
}

# Create log from one message exchange
def createMsgLog(userId, botId, userMsg, botMsg, status = "success", statusDetails = ""):
    timestamp = str(datetime.datetime.now())
    content = {"userMsg" : userMsg, "botMsg" : botMsg}
    log = { "entryType" : "msg", "owner" : userId, "bot" : botId, "datetime" : timestamp, "content" : content, "status" : {"tag" : status}}

    saveLog(log)

# Validate and save json logs
def saveLog(jsonLog):
    try:
        # Validate entry
        validate(jsonLog, schema)
        # Open client to database
        client = MongoClient('mongodb://localhost:27017/')
        db = client.test_log
        collection = db.test_collection
        post_id = db.posts.insert_one(jsonLog).inserted_id
        print("Correctly added log with ID " + post_id)
    except Exception as e:
        print("Invalid log")
        print(jsonLog)
        print()
        print(e)
