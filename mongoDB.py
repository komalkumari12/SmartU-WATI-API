

from flask import Flask
from flask_pymongo import pymongo
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