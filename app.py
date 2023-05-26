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
from LanguagePreference import languagePreference
from validate_Input import validate_string_input


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

def makeOtherOptionTrue(isOtherOption):
    isOtherOption = True

@app.route('/sendMessage',methods=["GET", "POST"])
def functionCall():
    data = request.json
    # print(data)
    # print(data['type'])
    # print(data)
    textByUser = data['text']
    phoneNumber = data['waId']
    senderName = data['senderName']


    if(textByUser == 'Hi' or textByUser == 'Hii' or textByUser == 'Hello' or textByUser == 'Hey'):
        welcomeMessage = 'Hi, Welcome to Krishi Clinic'
        sendSessionMessage(welcomeMessage)
        cropList()
        print("text By User : "  + textByUser)

    else:   
        print('HEllo00')
        # print(textByUser)
        if textByUser is None:
            print('USer response now : ')
            user_response = data['listReply']['title']
            print(user_response)

            if(user_response != 'Other'):
                print('User Input is a Crop')
                mongoDB.db.user.insert_one({"phoneNumber":918355882259, "senderName": senderName,"already":1,"next":2, "Crop Name": user_response})

                nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
                print(nextQuestion)

                question = mongoDB.db2.questions.find_one({"no":str(nextQuestion)})['question']
                print(question)
                sendSessionMessage(question)
        
            elif(user_response == 'Other'):
                print('User selected Other Option')
                mongoDB.db.user.insert_one({"phoneNumber":918355882259, "senderName": senderName,"already":0,"next":1, "Crop Name": user_response})

                nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
                print(nextQuestion)

                question = mongoDB.db2.questions.find_one({"no":str(nextQuestion)})['question']
                print(question)
                sendSessionMessage(question)

        else :
            isWrongInput = False
            print("In the else block")
            print(textByUser)

            cropName= mongoDB.db['user'].find_one({'phoneNumber':918355882259})['Crop Name']
            print(cropName)
            nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
            print(nextQuestion)

            # if cropName == 'Other' and nextQuestion == 1:
            #     print("Crop is stored")
                
            if(nextQuestion < 5):
                print("Inside nextQuestion if Statement")
                question = mongoDB.db2.questions.find_one({"no":str(nextQuestion)})['question']
                print(question)
                dataType = mongoDB.db2.questions.find_one({"no":str(nextQuestion)})['dataType']
                print(dataType)

                if nextQuestion == 3 and (textByUser == 'English' or textByUser == 'Hindi' or textByUser == 'Marathi'):
                    print('Store language in DB')
                    print('language input by user  : '  + textByUser)
                    # Store Language in DB
                    mongoDB.db.user.update_one({"phoneNumber": 918355882259},{"$inc": {"already": 1, "next": 1},"$set": {"language": textByUser}},upsert=True)

                else :
                # Store Response By User
                    if(dataType == "String"):
                        print('Input should be a String : ')
                        if(textByUser.isnumeric() == False)  :  
                            print("Input is a String")
                            mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                            print('Answer sent by USer : ' + textByUser)
                        else : 
                            isWrongInput = True
                    elif(dataType == "Number"):
                        print('Input should be a Number : ')
                        if(textByUser.isnumeric() == True)  :  
                            print("Input is a Number")
                            mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                            print('Answer sent by USer : ' + textByUser)
                        else : 
                            isWrongInput = True        
                    else:
                        print('Here')
                        mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                        print('Answer sent by USer : ' + textByUser)

                # Asking Next Question
                if(isWrongInput == False):
                    nextQuestion += 1
                    if(nextQuestion == 3):
                        print('Ask User for his language preference')
                        language = languagePreference()
                        print(language)

                    elif nextQuestion < 5 and isWrongInput == False:
                        question = mongoDB.db2.questions.find_one({"no":str(nextQuestion)})['question']
                        print(question)
                        sendSessionMessage(question)
                elif isWrongInput == True:
                    sendSessionMessage("Input format is not correct")

            else:
                    sendSessionMessage('All Questions are asked')

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