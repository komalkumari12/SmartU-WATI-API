import flask
import requests
import json
from flask import Flask,request
from flask import jsonify
from flask_cors import CORS, cross_origin
from SessionMessage import sendSessionMessage
from SendImageFile import sendImageFile
import mongoDB
from readImage import read_image
from storeImage import store_image
from downloadImage import downloadImage


from dotenv import load_dotenv
import os 
load_dotenv()
port = os.getenv("PORT")

# from dotenv import dotenv_values
# import os 
# config = dotenv_values(".env")

from dotenv import load_dotenv
import os 
load_dotenv()
app = Flask(__name__)

CORS(app)


@app.route('/')
def DefaultRoute():
    return "Home Page"

@app.route('/sendMessage',methods=["GET", "POST"])
def functionCall():
    data = request.json
    print(data['data'])
    textSentByUser = data['text']
    phoneNumber = data['waId']

    if(data['type']=='text'):
        print('  User sent a text  ')
        response = mongoDB.db.questions.find_one({"Q":textSentByUser})
        # print(response)

        print(textSentByUser)

        if(textSentByUser=='Hi'):
            question = mongoDB.db.questions.find_one({"no":"1"})
            print(question['question'])
            sendSessionMessage(question['question'])
            mongoDB.db.user.update_one({"phoneNumber":phoneNumber,"already":0,"next":1},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":question,"A":textSentByUser}}},upsert=True)
            # mongoDB.db.user.update_one({"phoneNumber":phoneNumber,"already":0,"next":1},{"$inc":{"already":1,"next":1}},upsert=True)
        else:
            nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':phoneNumber})['next']
            print(nextQuestion)
            if(nextQuestion<=4):
                question = mongoDB.db.questions.find_one({"no":str(nextQuestion)})['question']
                print(question)
                prevQuestion = mongoDB. db.questions.find_one({"no" : str(nextQuestion-1)})['question']
                sendSessionMessage(question)
                mongoDB.db.user.update_one({"phoneNumber":phoneNumber},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":prevQuestion,"A":textSentByUser}}},upsert=True)
            else:
                sendSessionMessage("Thankyou for your Time")   
        
       
    if(data['type']=='image'):
        print('  User Sent an Image  ')

        imgUrl = downloadImage(data['data'])
        store_image(phoneNumber , "./sample.jpg")
        # storedImage = retrieve_image()
        # print(storedImage)

        sendImageFile(imgUrl, data)
        return "ok"

    return "Okkk"

@app.route('/add-question', methods=['POST'], endpoint='add_question')
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


if __name__ == '__main__':  
    app.run(debug=True, port=port)