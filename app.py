import flask
import requests
import json
from flask import Flask,request
# from flask_pymongo import PyMongo
from SessionMessage import sendSessionMessage
from SendImageFile import sendImageFile
import mongoDB

from dotenv import load_dotenv
import os 
load_dotenv()
port = os.getenv("PORT")

from dotenv import load_dotenv
import os 
load_dotenv()
# MONGO_URI = os.getenv("MONGO_URI")
app = Flask(__name__)

# mongodb_client = PyMongo(app, uri=MONGO_URI)
# db = mongodb_client.db

textSentByUser = ""

@app.route('/')
def DefaultRoute():
    return "Home Page"

@app.route('/sendMessage',methods=["GET", "POST"])
def functionCall():
    data = request.json
    # # print(data['type'])
    textSentByUser = data['text']
    phoneNumber = data['waId']
    print(textSentByUser)
    # print(data)

    if(data['type']=='text'):
        response = mongoDB.db.questions.find_one({"Q":textSentByUser})
        if response == None:
            message = sendSessionMessage('Sorry! I dont know the answer of this question.')
        else:
            message = sendSessionMessage(response['A'])
    
        mongoDB.db.askedQuestion.update_one({"phoneNumber":phoneNumber
        },{"$push":{"questions":{"Q":textSentByUser,"A":message}}},upsert=True)
        return message
    if(data['type']=='image'):
        return sendImageFile()

@app.route('/add-question', methods=['POST'])
def add_question():
    try:
        data = request.json
        
        # Get the question and answer from the JSON data
        question = data.get('Q')
        answer = data.get('A')
        
        # Insert the question and answer into the MongoDB collection
        mongoDB.db.questions.insert_one({'Q': question, 'A': answer})
        
        return {'message': 'Question added successfully!'}
    except Exception as e:
        return {'error': str(e)}


# @app.route("/test")
# def test():
#     print("hello komal")
#     mongoDB.db.collection.insert_one({"name00" : "komal"})
#     return "Connected to the data base!"

if __name__ == '__main__':  
    app.run(debug=True, port=port)