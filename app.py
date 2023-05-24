import flask
import requests
import json
from flask import Flask,request
from flask import jsonify
from flask_cors import CORS, cross_origin
from SessionMessage import sendSessionMessage
from SendImageFile import sendImageFile
from sendInteractiveButton import sendInteractiveButtonMessage
import mongoDB
from storeImage import store_image
from downloadImage import downloadImage
from HindiContent import HindiContent1
from HindiContent import HindiContent2
from EnglishContent import EnglishContent1
from EnglishContent import EnglishContent2
from MarathiContent import MarathiContent1
from MarathiContent import MarathiContent2
from cropList import cropList


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
    # print(data)
    # print(data['type'])

    textByUser = data['text']
    phoneNumber = data['waId']
    senderName = data['senderName']
    language = ""

    user_response = ""

    # if textByUser.isnumeric():
    #     print("Input is a number : " + textByUser)

    if(data['type'] == 'text'):

        if(textByUser == 'Hi'):
            langQuestion = 'What is your preferred Language ??'
            # sendSessionMessage(langQuestion)
            user_response = sendInteractiveButtonMessage()
            print("User Response : " + user_response)
            print("TextByUser : " + textByUser)

        elif(textByUser == 'English'):
            print('Content 1 of English is called')
            EnglishContent1(textByUser, senderName)

        elif(textByUser == 'Hindi'):
            print('Content 1 of Hindi is called')
            HindiContent1(textByUser, senderName)

        elif(textByUser == 'Marathi'):
            print('Content 1 of Marathi is called')
            MarathiContent1(textByUser, senderName)        
        
        else:
            print('Content 2 of  preferred language is called')
            language = mongoDB.db.user.find_one({"phoneNumber" : 918355882259})['language']
            print(language)

            if(language == 'English'):
                EnglishContent2(textByUser)

            elif(language == 'Hindi'):
                    HindiContent2(textByUser)

            elif(language == 'Marathi'):
                MarathiContent2(textByUser)

    if(data['type']=='image'):
        print('  User Sent an Image  ')

        imgUrl = downloadImage(data['data'])
        image_url_MongoDB = store_image(918355882259 , "./sample.jpg")
        # print(image_url_MongoDB)
        sendImageFile(imgUrl)

        return "ok"    
    return "Ok" 

# @app.route('/sendMessage',methods=["GET", "POST"])
# def functionCall():
#     data = request.json
#     print(data)
#     print(data['type'])

#     textByUser = data['text']
#     phoneNumber = data['waId']
#     senderName = data['senderName']
#     language = ""

#     if(textByUser == 'Hi' or textByUser == 'Hii' or textByUser == 'Hello' or textByUser == 'Hey'):
#         welcomeMessage = 'Hi, Welcome to Krishi Clinic'
#         sendSessionMessage(welcomeMessage)
#         user_response =  cropList()
#         print(user_response)
#     return "ok"    

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