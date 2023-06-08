import flask
import requests
import json
from flask import Flask,request
from flask import jsonify
# from flask_cors import CORS, cross_origin
from SessionMessage import sendSessionMessage
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
import mongoDB as mdb
from kcImage import execute

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
    print(data['type'])
    textByUser = data['text']
    phoneNumber = data['waId']
    senderName = data['senderName']

    if(textByUser == 'KrishiClinicTest'):
        welcomeMessage = 'Hi, Welcome to Krishi Clinic'
        sendSessionMessage(welcomeMessage)

        language = languagePreference()
        print(language)
    
    elif(data['type'] == 'video' or data['type'] == 'document'):
        print('User sent a video or a document')
        sendSessionMessage('Only send images')

    elif(data['type'] == 'image'):
        print('Kc_upload sent a Image')

        image = data['data']
        
        new_image_url = data.get('data')
        # execute(new_image_url)
        execute(data)
        # EnglishContent2(data, image)

    elif(data['type'] == 'audio'):
        print('Kc_upload input is a Audio')

        audio = data['data']
        print(audio)

        
        language = mdb.db.kc_upload.find_one({"phoneNumber": 918355882259})["language"]

        if(language == 'English'):
            EnglishContent2(data, audio)
        elif(language == 'हिंदी'):
            HindiContent2(data, audio)
        elif(language == 'मराठी'):  
            MarathiContent2(data, audio)

    else:
        if textByUser is None and data['listReply']!=None:
        #     print(textByUser)
            print('HEllo00')

            user_response = data['listReply']['title']
            print("Kc_upload input is : " + user_response)

            if user_response != 'Other' and user_response != 'अन्य' and user_response != 'इतर':
                print('User Input is a Crop')
                mdb.db.kc_upload.update_one({"phoneNumber": 918355882259}, {"$set": {"already": 1, "next": 2, "Crop Name": user_response}}, upsert=True)

                nextQuestion = mdb.db['kc_upload'].find_one({'phoneNumber':918355882259})['next']
                print(nextQuestion)

                language = textByUser

                language = mdb.db.kc_upload.find_one({"phoneNumber": 918355882259})["language"]

                if(language == 'English'):
                    print('Language is English')
                    EnglishContent0(nextQuestion)
                elif(language == 'हिंदी'):
                    print('Language is हिंदी')
                    HindiContent0(nextQuestion)
                elif(language == 'मराठी'):
                    print('Language is मराठी')   
                    MarathiContent0(nextQuestion) 
        
            elif(user_response == 'Other' or user_response == 'अन्य' or user_response == 'इतर'):
                print('User selected Other Option')
   
                mdb.db.kc_upload.update_one({"phoneNumber": 918355882259}, {"$set": {"already": 0, "next": 1, "Crop Name": user_response}}, upsert=True)
                nextQuestion = mdb.db['kc_upload'].find_one({'phoneNumber':918355882259})['next']
                print(nextQuestion)

                language = mdb.db.kc_upload.find_one({"phoneNumber": 918355882259})["language"]

                if(language == 'English'):
                    print('Language is English')
                    EnglishContent0(nextQuestion)
                elif(language == 'हिंदी'):
                    print('Language is हिंदी')
                    HindiContent0(nextQuestion)
                elif(language == 'मराठी'):
                    print('Language is मराठी')   
                    MarathiContent0(nextQuestion)

        else:

            if textByUser == 'Yes' or textByUser == 'हाँ' or textByUser == 'erreer' or textByUser == 'No' or textByUser == 'नहीं' or textByUser == 'नाही':
  
                language = mdb.db.kc_upload.find_one({"phoneNumber": 918355882259})["language"]
                print(language)
                nextQuestion = mdb.db.kc_upload.find_one({'phoneNumber':918355882259})['next']
                print(nextQuestion)

                # More Queries for USers to input
                print('Kc_upload Response for more questions is : ' + textByUser)
                print('Entered here in yes no block')
                if(nextQuestion==3 and textByUser == 'Yes' or  textByUser == 'हाँ' or textByUser == 'होय'):

                    print('Kc_upload selected a yes')
                    language = mdb.db.kc_upload.find_one({"phoneNumber": 918355882259})["language"]
                    print(language)

                    if(language == 'English'):
                        sendSessionMessage("Report diseases or problems on your crop (send by typing using your keyboard, or select the mic option on the keyboard and send a voice recording in less than a minute) ")
                    elif(language == 'हिंदी'):
                        print('Entered into हिंदी Content')
                        sendSessionMessage('अिनी नारांगी फसल की बीमाररयोां या समस्ाओां की जानकारी दे (अिने कीबोडड का उियोग करके टाइि करके भेजें, या कीबोडड िर माइक का पवकल्प चुनें और एक पमनट से भी कम समय में आवाज ररकॉडड करके भेजें )')
                    elif(language == 'मराठी'):
                        sendSessionMessage('तुमच्या सांत्र्याच्या पिकावरील रोग पकांवा समस्ाांबद्दल मापहती द्या (तुमच्या कीबोडडच्या मदतीने मराठी, पहांदी पकांवा इांक्लिशमध्ये टाईि करून िाठवा, अथवा कीबोडड वरील माइकचा ियाडय पनवडून एक पमपनटािेक्षा कमी वेळात आवाज रेकॉडड करून िाठवा)')

                elif(nextQuestion==3 and textByUser == 'No' or textByUser == 'नहीं' or textByUser == 'नाही'):
                    print('Kc_upload selected a yes')

                    language = mdb.db.kc_upload.find_one({"phoneNumber": 918355882259})["language"]
                    print(language)

                    if(language == 'English'):
                        sendSessionMessage('We have received information about the problem/disease in your Crop, please send two-three photos of the crop')
                    elif(language == 'हिंदी'):
                        sendSessionMessage('हमें आिके सांतरे की समस्ा/बीमारी के बारे में सूचना प्राप्त हुई है, कृिया सांबांपधत सांतरे के दो-तीन फोटो भेजें।')
                    elif(language == 'मराठी'):
                        sendSessionMessage('आम्हाला तुमच्या सांत्र्यामधील समस्ा/ रोग पवषयक मापहती पमळाली आहे, कृिया त्या सांबांपधत सांत्र्याचे दोन-तीन फोटो काढून िाठवा.')
                
                    
            elif (textByUser == 'English' or textByUser == 'हिंदी' or textByUser == 'मराठी'):
                print('Store language in DB')
                print('language input by kc_upload  : '  + textByUser)
                # Store Language in DB
                # image_url = {""}
                mdb.db.kc_upload.insert_one({"phoneNumber": 918355882259,"senderName": senderName,"language": textByUser,"userflow":"KC", "sent_image": "", "image_url": [], "stored_image": [] ,"cloudinary_images": [], "cropQuestions" : []})
                language = mdb.db.kc_upload.find_one({"phoneNumber": 918355882259})["language"]
                # mdb.create_record(918355882259,senderName,textByUser,"","",textByUser,"")
                language = textByUser

                if(language == 'English'):
                    print('Language is English')
                    EnglishContent1()
                elif(language == 'हिंदी'):
                    print('Language is हिंदी')
                    HindiContent1()
                elif(language == 'मराठी'):
                    print('Language is मराठी')   
                    MarathiContent1() 
            
            else:
                language = mdb.db.kc_upload.find_one({"phoneNumber": 918355882259})["language"]

                if(language == 'English'):
                    print('Language is English')
                    EnglishContent2(data, textByUser)
                elif(language == 'हिंदी'):
                    print('Language is हिंदी')
                    HindiContent2(data, textByUser)
                elif(language == 'मराठी'):
                    print('Language is मराठी')
                    MarathiContent2(data, textByUser)

    return "ok"    

@app.route('/add-question', methods=['POST'], endpoint='add_question')
def add_question():
    try:
        data = request.json
        # Get the question and answer from the JSON data
        question = data.get('Q')
        answer = data.get('A')

        # Insert the question and answer into the mdb collection
        mdb.db.questions.insert_one({'Q': question, 'A': answer})
        
        return {'message': 'Question added successfully!'}
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':  
    app.run(debug=True, port=port)