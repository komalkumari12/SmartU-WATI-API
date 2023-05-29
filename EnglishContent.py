import mongoDB  
from SessionMessage import sendSessionMessage
from cropList import cropListEnglish
from urllib.parse import urlparse
from  downloadAudio import downloadAudio
from MoreQuestions import moreQuestions

def EnglishContent0(nextQuestion):
    question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
    print(question)
    sendSessionMessage(question)

def EnglishContent1():
    cropListEnglish()

    return "ok"

def EnglishContent2(data, textByUser):
    dataSent = data['type']
    print(dataSent)
    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
    print(nextQuestion)
    alreadyAsked = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['already']
    print(alreadyAsked)   
    CropValue = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['Crop Name']
    print("Crop Name is  : " + CropValue)

    
    if(dataSent == 'text'):
        print('Data sent is a text')
        print(nextQuestion)

        if(nextQuestion < 5):
            print("Inside nextQuestion if Statement")
            question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
            print(question)
            dataType = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['dataType']
            print(dataType)

            # Store Response By User
            if(dataType == "String"):
                print('Input should be a String : ')
                if(textByUser.isnumeric() == False)  :  
                    print("Input is a String")
                    if(alreadyAsked == 0):
                        print('Store value of Crop in a new field')
                        print('Text by USer is :  ' + textByUser)
                        mongoDB.db.user.update_one({'phoneNumber': 918355882259 },{'$set': {'Other': textByUser},"$inc":{"already":1,"next":1}},upsert=True)
                    else:
                        mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                        print('Answer sent by USer : ' + textByUser)

                    nextQuestion += 1
                    if nextQuestion < 5 :
                        question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
                        print(question)
                        sendSessionMessage(question)

                else : 
                    sendSessionMessage('Incorrect Input.... Input a string')
            elif(dataType == "Number"):
                print('Input should be a Number : ')
                if(textByUser.isnumeric() == True)  :  
                    print("Input is a Number")
                    textByUserNumber = int(textByUser)
                    if(alreadyAsked == 1):
                        print('Store value of Crop in a new field')
                        print('Text by USer is :  ' + textByUser)
                        mongoDB.db.user.update_one({'phoneNumber': 918355882259 },{'$set': {'Acre': textByUserNumber},"$inc":{"already":1,"next":1}},upsert=True)
                    else:
                        mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                        print('Answer sent by USer : ' + textByUser)

                    nextQuestion += 1
                    if nextQuestion < 5 :
                        question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
                        print(question)
                        sendSessionMessage(question)
                else : 
                    sendSessionMessage('Incorrect Input.... Input a Number')         
            else:
                print('Input can be a string or Audio')
                mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                print('Answer sent by User : ' + textByUser)

        else:
            sendSessionMessage('Thankyou for your Time !!')   

    elif(dataSent == 'audio'):
        print('Media is Audio')
        audio = data['data']
        downloadAudio(audio)
        print(audio)
        nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
        print(nextQuestion)
        # question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
        # print(question)

        # mongoDB.db.user.update_one({"phoneNumber": 918355882259},{"$set": {"audio_url": audio},"$inc": {"already": 1, "next": 1}},upsert=True)
          
        length = len(mongoDB.db.user.find_one({'phoneNumber': 918355882259}).get('audio_urls', []))
        print('Length of Audio Url is : ') 
        print(length)

        mongoDB.db.user.update_one({'phoneNumber': 918355882259},{'$push': {'audio_urls': {'$each': [audio]}},'$inc': {'already': 1, 'next': 1}},upsert=True)  
        
        if(length <= 1):
            moreQuestions()
    return "ok"             
