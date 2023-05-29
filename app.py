import flask
import requests
import json
from flask import Flask,request
from flask import jsonify
# from flask_cors import CORS, cross_origin
from SessionMessage import sendSessionMessage
from SendImageFile import sendImageFile
from sendInteractiveButton import sendInteractiveButtonMessage
import mongoDB
from storeImage import store_image
from downloadImage import downloadImage
from HindiContent import HindiContent0
from HindiContent import HindiContent1
from HindiContent import HindiContent2
from EnglishContent import EnglishContent0
from EnglishContent import EnglishContent1
from EnglishContent import EnglishContent2
from MarathiContent import MarathiContent0
from MarathiContent import MarathiContent1
from MarathiContent import MarathiContent2
from LanguagePreference import languagePreference


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


# CORS(app)

@app.route('/')
def DefaultRoute():
    return "Home Page"

@app.route('/sendMessage',methods=["GET", "POST"])
def functionCall():
    data = request.json
    print(data)
    print(data['type'])
    textByUser = data['text']
    phoneNumber = data['waId']
    senderName = data['senderName']

    if(textByUser == 'KrishiClinicTest'):
        welcomeMessage = 'Hi, Welcome to Krishi Clinic'
        sendSessionMessage(welcomeMessage)

        language = languagePreference()
        print(language)

    if(data['type'] == 'audio'):
        print('User input is a Audio')

        audio = data['data']
        print(audio)

        
        language = mongoDB.db.user.find_one({"phoneNumber": 918355882259})["language"]

        if(language == 'English'):
            EnglishContent2(data, audio)
        elif(language == 'Hindi'):
            HindiContent2(data, audio)
        elif(language == 'Marathi'):  
            MarathiContent2(data, audio)

    else:
        if textByUser is None:
        #     print(textByUser)
            print('HEllo00')
            user_response = data['listReply']['title']
            print("User input is : " + user_response)

            if user_response != 'Other' and user_response != 'अन्य' and user_response != 'इतर':
                print('User Input is a Crop')
                mongoDB.db.user.update_one({"phoneNumber": 918355882259}, {"$set": {"already": 1, "next": 2, "Crop Name": user_response}}, upsert=True)

                nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
                print(nextQuestion)

                language = textByUser

                language = mongoDB.db.user.find_one({"phoneNumber": 918355882259})["language"]

                if(language == 'English'):
                    print('Language is English')
                    EnglishContent0(nextQuestion)
                elif(language == 'Hindi'):
                    print('Language is Hindi')
                    HindiContent0(nextQuestion)
                elif(language == 'Marathi'):
                    print('Language is Marathi')   
                    MarathiContent0(nextQuestion) 
        
            elif(user_response == 'Other' or user_response == 'अन्य' or user_response == 'इतर'):
                print('User selected Other Option')
   
                mongoDB.db.user.update_one({"phoneNumber": 918355882259}, {"$set": {"already": 0, "next": 1, "Crop Name": user_response}}, upsert=True)
                nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
                print(nextQuestion)

                language = mongoDB.db.user.find_one({"phoneNumber": 918355882259})["language"]

                if(language == 'English'):
                    print('Language is English')
                    EnglishContent0(nextQuestion)
                elif(language == 'Hindi'):
                    print('Language is Hindi')
                    HindiContent0(nextQuestion)
                elif(language == 'Marathi'):
                    print('Language is Marathi')   
                    MarathiContent0(nextQuestion)

        else:
            if (textByUser == 'English' or textByUser == 'Hindi' or textByUser == 'Marathi'):
                print('Store language in DB')
                print('language input by user  : '  + textByUser)
                # Store Language in DB
                mongoDB.db.user.insert_one({"phoneNumber":918355882259, "senderName": senderName, "language": textByUser})

                language = mongoDB.db.user.find_one({"phoneNumber": 918355882259})["language"]

                if(language == 'English'):
                    print('Language is English')
                    EnglishContent1()
                elif(language == 'Hindi'):
                    print('Language is Hindi')
                    HindiContent1()
                elif(language == 'Marathi'):
                    print('Language is Marathi')   
                    MarathiContent1() 
            
            else:
                language = mongoDB.db.user.find_one({"phoneNumber": 918355882259})["language"]

                if(language == 'English'):
                    print('Language is English')
                    EnglishContent2(data, textByUser)
                elif(language == 'Hindi'):
                    print('Language is Hindi')
                    HindiContent2(data, textByUser)
                elif(language == 'Marathi'):
                    print('Language is Marathi')
                    MarathiContent2(data, textByUser)

    return "ok"    

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