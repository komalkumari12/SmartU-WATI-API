import flask
import requests
import json
from flask import Flask,request
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
app = Flask(__name__)


textSentByUser = ""

@app.route('/')
def DefaultRoute():
    return "Home Page"

@app.route('/sendMessage',methods=["GET", "POST"])
def functionCall():
    data = request.json
    print(data)
    textSentByUser = data['text']
    phoneNumber = data['waId']

    if(data['type']=='text'):
        response = mongoDB.db.questions.find_one({"Q":textSentByUser})

        if(textSentByUser=='Hi'):
            question = mongoDB.db.questions.find_one({"no":"1"})
            sendSessionMessage(question['question'])
            mongoDB.db.user.update_one({"phoneNumber":phoneNumber,"state":"","country":"","already":0,"next":1},{"$inc":{"already":1,"next":1}},upsert=True)
        else:
            nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':phoneNumber})['next']
            if(nextQuestion<4):
                question = mongoDB.db.questions.find_one({"no":str(nextQuestion)})['question']
                sendSessionMessage(question)
                mongoDB.db.user.update_one({"phoneNumber":phoneNumber},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":question,"A":textSentByUser}}},upsert=True)
            else:
                sendSessionMessage("Thankyou for your Time")    
       
    if(data['type']=='image'):
        return sendImageFile('https://live-server-101955.wati.io/api/file/showFile?fileName=data/images/5303e57b-bbe6-455e-8d1c-04e9e4ed9912.jpg')


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