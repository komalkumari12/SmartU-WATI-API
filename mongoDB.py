# import flask
# from flask import Flask,request
# from dotenv import load_dotenv
# import os 
# load_dotenv()
# import json
# from flask import Flask , request, redirect, url_for
# # from flask_mongoengine import MongoEngine

# # from flask_pymongo import 
# MONGO_URI = os.getenv("MONGO_URI")
# app = Flask(__name__)

# mongodb_client = PyMongo(app, uri=MONGO_URI)
# db = mongodb_client.db

# class addQues(db.Document):
#     Q = db.StringField(required=True)
#     A = db.StringField()

# def addQuestionsToDB():
#     db.userInput.insert_one({"Q" : 'Question', "A" : 'Answer to user'})
#     return flask.jsonify(message="success")





# from flask_p  ymongo import PyMongo
# import flask
# from dotenv import load_dotenv
# import os 
# load_dotenv()

# app = flask.Flask(__name__)

# MONGO_URI = os.getenv("MONGO_URI")
# mongodb_client = PyMongo(app, uri="MONGO_URI")
# db = mongodb_client.db

# @app.route("/add_ques")
# def addQuestionsToDB():
#     db.addQues.insert_one({'Q': "Question", 'A': "Answer"})
#     return flask.jsonify(message="success")



from flask import Flask
from flask_pymongo import pymongo
from app import app

from dotenv import load_dotenv
import os 
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

CONNECTION_STRING = MONGO_URI

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')