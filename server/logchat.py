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
            "enum": ["msg", "admin", "train"]
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
                    "description" : "The intent extracted from userMsg or specified by user",
                    "type" : "string"
                },
                "botMsg" : {
                    "description" : "The answer provided by the bot",
                    "type" : "string"
                },
                "oldPattern" : {
                    "description" : "The pattern to replace",
                    "type" : "string"
                },
                "newPattern" : {
                    "description" : "The pattern-s to add or put in place of oldPattern",
                    "type" : ["string", "array"]
                },
                "oldResponse" : {
                    "description" : "The response to replace",
                    "type" : "string"
                },
                "newResponse" : {
                    "description" : "The response-s to add or put in place of oldResponse",
                    "type" : ["string", "array"]
                },
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
    "required": ["entryType", "owner", "bot", "datetime", "status"]
}

# Create log from one message exchange
def createMsgLog(userId, botId, userMsg, intent, botMsg, status = "success", statusDetails = ""):
    timestamp = str(datetime.datetime.now())
    content = {"userMsg" : userMsg, "intent" : intent, "botMsg" : botMsg}
    log = { "entryType" : "msg", "owner" : userId, "bot" : botId, "datetime" : timestamp, "content" : content, "status" : {"tag" : status}}
    if len(statusDetails) > 0:
        log["status"]["details"] = statusDetails

    logId = saveLog(log)
    return logId

def registerComplaint(logId):
    search = {"_id" : logId}
    update = {"status" : {"tag" : "warning", "details" : "User complaint"}}
    # Open client to database
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test_log
    # Update log in database
    db.posts.update_one(search, {"$set" : update})

def createIntentsModifLog(userId, botId, intent, newPattern = "", oldPattern = "", newResponse = "", oldResponse = "", patterns = [], responses = [], status = "success", statusDetails = ""):
    timestamp = str(datetime.datetime.now())

    # Create content depending on the type of modification
    content = {"intent" : intent}
    if len(oldPattern) > 0:
        content["oldPattern"] = oldPattern # Replace a pattern
    elif len(oldResponse) > 0:
        content["oldResponse"] = oldResponse # Replace a response

    if len(newPattern) > 0:
        content["newPattern"] = newPattern # Add or replace a pattern
    elif len(newResponse) > 0:
        content["newResponse"] = newResponse # Add or replace a response

    if len(patterns) > 0: # Add an intent
        content["newPattern"] = patterns
        content["newResponse"] = responses

    # Create full log
    log = {"entryType" : "admin", "owner" : userId, "bot" : botId, "datetime" : timestamp, "content" : content, "status" : {"tag" : status}}
    if len(statusDetails) > 0:
        log["status"]["details"] = statusDetails

    logId = saveLog(log)
    return logId

# Create and save log for train/retrain actions
def registerRetrain(userId, botId, status = "success", statusDetails = ""):
    timestamp = str(datetime.datetime.now())
    log = {"entryType" : "train", "owner": userId, "bot" : botId, "datetime" : timestamp, "status" : {"tag" : status}}
    if len(statusDetails) > 0:
        log["status"]["details"] = statusDetails
    logId = saveLog(log)
    return logId


# Validate and save json logs
def saveLog(jsonLog):
    try:
        # Validate entry
        validate(jsonLog, schema)
        # Open client to database
        client = MongoClient('mongodb://localhost:27017/')
        db = client.test_log
        collection = db.test_collection
        # Save log in database
        logId = db.posts.insert_one(jsonLog).inserted_id
        return logId
    except Exception as e:
        print("Invalid log")
        print(jsonLog)
        print()
        print(e)
