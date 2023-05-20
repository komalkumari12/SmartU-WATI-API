import requests
import mongoDB
from SessionMessage import sendSessionMessage
from SendImageFile import sendImageFile
from storeImage import store_image
from downloadImage import downloadImage

def content(language):
    contentTable = language
    # print(textByUser)

    if(contentTable == 'Hindi'):
        print('Connected with Hindi content collection')
    if(contentTable == 'Marathi'):
        print('Connected with Marathi content collection')
    if(contentTable == 'English'):
        print('Connected with English content collection')

        # question = mongoDB.db2.English.find_one({"no":"1"})
        # print(question['question'])
        # print('Hello question')
  
    return contentTable

    # data = requests.json
    # print(data['data'])
    # textSentByUser = data['text']
    # phoneNumber = data['waId']

    # # user_response = data['actions'][0]['text']
    # # print('User response:', user_response)

    # if(data['type']=='text'):
    #     print('  User sent a text  ')
    #     response = mongoDB.db.questions.find_one({"Q":textSentByUser})
    #     # print(response)

    #     print(textSentByUser)

    #     if(textSentByUser=='Hi'):
    #         question = mongoDB.db.questions.find_one({"no":"1"})
    #         print(question['question'])
    #         sendSessionMessage(question['question'])
    #         mongoDB.db.user.update_one({"phoneNumber":phoneNumber, "language":"","already":0,"next":1},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":question,"A":textSentByUser}}},upsert=True) 
    #     else:
    #         nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':phoneNumber})['next']
    #         print(nextQuestion)
    #         if(nextQuestion<=4):
    #             question = mongoDB.db.questions.find_one({"no":str(nextQuestion)})['question']
    #             prevQuestion = mongoDB. db.questions.find_one({"no" : str(nextQuestion-1)})['question']
    #             sendSessionMessage(question)
    #             mongoDB.db.user.update_one({"phoneNumber":phoneNumber},{"$inc":{"already":1,"next":1},"$push":{"questions":{"Q":prevQuestion,"A":textSentByUser}}},upsert=True)
    #         else:
    #             sendSessionMessage("Thankyou for your Time")   

    #     return "okkk"    
       
    # if(data['type']=='image'):
    #     print('  User Sent an Image  ')

    #     imgUrl = downloadImage(data['data'])
    #     image_url_MongoDB = store_image(phoneNumber , "./sample.jpg")
    #     # print(image_url_MongoDB)
    #     sendImageFile(imgUrl)

    #     return "ok"

    