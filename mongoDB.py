from flask import Flask
from flask_pymongo import pymongo
from pymongo import MongoClient
import pymongo
import numpy as np
from bson import ObjectId

# from app import app

from dotenv import dotenv_values
import os 
config = dotenv_values(".env")

# print(config['MONGO_URI'])

# MONGO_URI = os.getenv("MONGO_URI")

MONGO_URI = config["MONGO_URI"]

CONNECTION_STRING = MONGO_URI

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
db2 = client.get_database('content')


def create_record(phone, name, image_url):
    try:
        client = pymongo.MongoClient()
        db = client["Krishi_Clinic"]
        collection = db["kc_upload"]

        user_data = {"userID": phone, "name": name, "sent_image":""}
        updated_status = {"$push": {"image_url": image_url, "stored_image": image_url}}

        result = collection.update_one(user_data, updated_status, upsert=True)

        if result.upserted_id:
            print("New record created.")

        else:
            print("Record updated.")
        return "Success"

    except Exception as e:
        print("create_record error", e)


def find_user(senderID):
    try:

        client = pymongo.MongoClient()
        db = client["Krishi_Clinic"]
        collection = db["kc_upload"]

        query = {"userID": senderID}

        print("query ", collection.find_one(query))
        return collection.find_one(query)

    except Exception as e:
        print("find_user error", e)

def retrieve_field(userID, field_name):
    try:
        client = pymongo.MongoClient()
        db = client["Krishi_Clinic"]
        collection = db["kc_upload"]
        doc = collection.find_one({'userID': userID})

        if doc:
            field = doc.get(field_name)
            return field

        else:
            query = "No document found."
            return query
            
    except Exception as e:
        print("find  error", e)
        
def update_image_url(userID,image_field, image_url):
    client = pymongo.MongoClient()
    db = client["Krishi_Clinic"]
    collection = db["kc_upload"]

    user_data = {"userID": userID}
    chat_log = {
        "$push": {image_field: 
                  {"$each":[image_url], "$position": 0}
                }
            }
                  
    result = collection.update_one(user_data, chat_log, upsert=True)
    print("update_image_field ", result)



def update_field_set(phone, field_name, field_value):
    try:
        client = pymongo.MongoClient()
        db = client["Krishi_Clinic"]
        collection = db["kc_upload"]

        user_data = {"userID": phone}
        updated_status = {"$set": {field_name: field_value}}

        collection.update_one(user_data, updated_status, upsert=True)
        print("update_field_set ", collection.update_one(user_data, updated_status, upsert=True))
        return 200
        # print("update_chat_status ", r)
    except Exception as e:
        print("update set", e)
