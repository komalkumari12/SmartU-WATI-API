import flask
import requests
import json
from flask import Flask,request
from flask import jsonify
from flask_cors import CORS, cross_origin
from SessionMessage import sendSessionMessage
from SendImageFile import sendImageFile
import mongoDB
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

# @app.route("/upload", methods=['POST'])
# @cross_origin()




# @app.route('/')
# def DefaultRoute():
#     return "Home Page"

@app.route('/sendMessage',methods=["GET", "POST"])
def functionCall():
    data = request.json
    print(data['data'])
    textSentByUser = data['text']
    phoneNumber = data['waId']

    if(data['type']=='text'):
        print('  User sent a text  ')
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
        imgUrl = downloadImage(data['data'])
        return sendImageFile(imgUrl)

# @app.route("/upload", methods=['POST'], endpoint='upload')
# def upload_file():
#   app.logger.info('in upload route')
#   data = request.json
#   print(data['type'])

#   cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
#     api_secret=os.getenv('API_SECRET'))
#   upload_result = None
#   if request.method == 'POST':
#     file_to_upload = request.files['file']
#     app.logger.info('%s file_to_upload', file_to_upload)
#     if file_to_upload:
#       upload_result = cloudinary.uploader.upload(file_to_upload)
#       app.logger.info(upload_result)
#       return jsonify(upload_result)


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


# @app.route("/test")
# def test():
#     print("hello komal")
#     mongoDB.db.collection.insert_one({"name00" : "komal"})
#     return "Connected to the data base!"

if __name__ == '__main__':  
    app.run(debug=True, port=port)