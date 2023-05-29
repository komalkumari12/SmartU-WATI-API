import mongoDB
from validate_Input import validate_string_input
from SessionMessage import sendSessionMessage
from cropList import cropListHindi
from  downloadAudio import downloadAudio

def HindiContent0(nextQuestion):
    question = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion)})['question']
    print(question)
    sendSessionMessage(question)

def HindiContent1():
    cropListHindi()

    return "ok"

def HindiContent2(data, textByUser):
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

        if(nextQuestion < 4):
            print("Inside nextQuestion if Statement")
            question = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion)})['question']
            print(question)
            dataType = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion)})['dataType']
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
                        question = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion)})['question']
                        print(question)
                        sendSessionMessage(question)

                else : 
                    sendSessionMessage('गलत इनपुट....इनपुट एक स्ट्रिंग')
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
                        mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUserNumber}}},upsert=True)
                        print('Answer sent by USer : ' + textByUser)

                    nextQuestion += 1
                    if nextQuestion < 5 :
                        question = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion)})['question']
                        print(question)
                        sendSessionMessage(question)
                else : 
                    sendSessionMessage('गलत इनपुट...कोई नंबर डालें')         
            else:
                print('Here')
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
        question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
        print(question)

        mongoDB.db.user.update_one({"phoneNumber": 918355882259},{"$set": {"audio_url": audio},"$inc": {"already": 1, "next": 1}},upsert=True)
       
    return "ok" 

    print(textByUser)  
    print('In last block')
    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']

    if(nextQuestion<=5):
        question = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion)})['question']
        prevQuestion = mongoDB. db2.Hindi.find_one({"no" : str(nextQuestion-1)})['question']
        dataType = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion-1)})['dataType']
        print(dataType)

        if(dataType == 'String'):
            print('Input should be a String : ')
            if(textByUser.isnumeric() == False)  : 
                print('Input is String')
                mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":prevQuestion,"A":textByUser}}},upsert=True)
                sendSessionMessage(question)
            else: 
                sendSessionMessage("Input format is not correct, Give a string as answer!!")
        else:
            print('dataType is Number')
            if(textByUser.isnumeric() == True)  :  
                print("Input is a Number")
                mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":prevQuestion,"A":textByUser}}},upsert=True)
                sendSessionMessage(question)
            else: 
                sendSessionMessage("Input format is not correct, Give a Number as answer!!")        
    else : 
        sendSessionMessage("Thankyou For Your Time !!")