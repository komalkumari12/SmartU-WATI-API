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
from content import content
from HindiContent import HindiContent1
from HindiContent import HindiContent2


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

languageDone = False


@app.route('/')
def DefaultRoute():
    return "Home Page"

@app.route('/sendMessage',methods=["GET", "POST"])
def functionCall():
    data = request.json
    # print(data)

    textByUser = data['text']
    phoneNumber = data['waId']
    senderName = data['senderName']
    language = ""

    if(textByUser == 'Hi'):
        langQuestion = 'What is your preferred Language ??'
        sendSessionMessage(langQuestion)

    elif(textByUser == 'English'):
        mongoDB.db.user.insert_one({"phoneNumber":918355882259, "senderName": senderName,"language": textByUser,"already":0,"next":1}) 

        language = mongoDB.db.user.find_one({"phoneNumber" : 918355882259, "senderName": senderName,"language": textByUser,})['language']
        print(language)

        nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
        print(nextQuestion)
        question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
        print(question)
        sendSessionMessage(question)
        mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":question,"A":textByUser}}},upsert=True)

    elif(textByUser == 'Hindi'):
        HindiContent1(textByUser, senderName)

    elif(textByUser == 'Marathi'):
        mongoDB.db.user.insert_one({"phoneNumber":918355882259, "senderName": senderName,"language": textByUser,"already":0,"next":1}) 

        language = mongoDB.db.user.find_one({"phoneNumber" : 918355882259, "senderName": senderName,"language": textByUser,})['language']
        print(language)

        nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
        print(nextQuestion)
        question = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion)})['question']
        print(question)
        sendSessionMessage(question)
        mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":question,"A":textByUser}}},upsert=True)        
        
    else:
        print('Heyyy')
        language = mongoDB.db.user.find_one({"phoneNumber" : 918355882259})['language']
        print(language)

        if(language == 'English'):
            print(textByUser)  
            print('In last block')
            nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']

            if(nextQuestion<=4):
                question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
                prevQuestion = mongoDB. db2.English.find_one({"no" : str(nextQuestion-1)})['question']

                sendSessionMessage(question)
                mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":prevQuestion,"A":textByUser}}},upsert=True)
            else : 
                sendSessionMessage("All Questions are completed !!")

        elif(language == 'Hindi'):
            HindiContent2(textByUser)

        elif(language == 'Marathi'):
            print(textByUser)  
            print('In last block')
            nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']

            if(nextQuestion<=4):
                question = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion)})['question']
                prevQuestion = mongoDB. db2.Marathi.find_one({"no" : str(nextQuestion-1)})['question']

                sendSessionMessage(question)
                mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":prevQuestion,"A":textByUser}}},upsert=True)
            else : 
                sendSessionMessage("Thankyou For Your Time !!")

        

        # nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
        # print(nextQuestion)
        # question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
        # print(question)

        

    # if(data['type']=='text'):
    #     print('  User sent a text  ')
    #     response = mongoDB.db.questions.find_one({"Q":textByUser})
    #     # print(response)

    #     print(textByUser)

    #     if(textByUser=='Hi'):
    #         # question = mongoDB.db.questions.find_one({"no":"1"})
    #         # print(question['question'])
    #         # sendSessionMessage(question['question'])
    #         question = "Hii, What is your preferred language ??"
    #         sendSessionMessage(question)
    #         mongoDB.db.user.update_one({"phoneNumber":phoneNumber, "language":textByUser,"already":0,"next":1},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":question,"A":textByUser}}},upsert=True) 
    #     else:

    #         nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':phoneNumber})['next']
            # print(nextQuestion)
            # if(nextQuestion<=4):
            #     question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
            #     prevQuestion = mongoDB. db2.English.find_one({"no" : str(nextQuestion-1)})['question']
            #     sendSessionMessage(question)
            #     mongoDB.db.user.update_one({"phoneNumber":phoneNumber},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":prevQuestion,"A":textByUser}}},upsert=True)
            # else:
    #             sendSessionMessage("Thankyou for your Time")   

    #     return "okkk" 



    # if(textByUser=='Hi'):
    #     sendSessionMessage('Hi, What is your preferred Language')
    # else:

    #     if(textByUser == 'English' or textByUser == 'Hindi' or textByUser == 'Marathi'):
    #         mongoDB.db.user.insert_one({"phoneNumber":918355882259, "senderName": senderName,"language": textByUser,"already":0,"next":1}) 
    #         contentCollection = content(textByUser)

    #         # doing just for english users now
    #         question = mongoDB.db2.English.find_one({"no":"1"})
    #         print(question['question'])
    #         print('First Question now')
    #         sendSessionMessage(question['question'])
    #         mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":question,"A":textByUser}}},upsert=True )

        # language = mongoDB.db.user.find_one({"phoneNumber" : 918355882259})['language']
        # if(language == 'English'): 
        #     print('answer now')
            
            
        #     nextQuestion = mongoDB.db2['English'].find_one({'phoneNumber':918355882259})['next']
        #     question = mongoDB.db.questions.find_one({"no":str(nextQuestion)})['question']
        #     print(question['question'])
        #     mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":question,"A":textByUser}}},upsert=True )
        #     sendSessionMessage(question['question'])
      


        # question = mongoDB.db2.English.find_one({"no":"1"})
        # print(question['question'])    

        # question = mongoDB.db.contentTable.find_one({"no":"1"})
        # print(contentTable['question'])
        # sendSessionMessage(contentTable['question'])  
        # mongoDB.db.user.update_one({"phoneNumber":phoneNumber, "language":"","already":0,"next":1},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":question,"A":textByUser}}},upsert=True )     

        # if(language == 'English'):
        #     print('Ask questions based on English content Collection')


    return "Ok"


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