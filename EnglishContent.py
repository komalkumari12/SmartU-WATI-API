import mongoDB  
from SessionMessage import sendSessionMessage
from cropList import cropList
from urllib.parse import urlparse

def EnglishContent0(nextQuestion):
    question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
    print(question)
    sendSessionMessage(question)

def EnglishContent1():
    cropList()

    return "ok"

def EnglishContent2(data, textByUser):
    dataSent = data['type']
    print(dataSent)
    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
    print(nextQuestion)   
    
    if(dataSent == 'text'):
        print('Data sent is a text')
        if(nextQuestion < 4):
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
                    mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                    print('Answer sent by USer : ' + textByUser)

                    nextQuestion += 1
                    if nextQuestion < 5 :
                        question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
                        print(question)
                        sendSessionMessage(question)

                else : 
                    sendSessionMessage('Incorrect Input....Input a String')
            elif(dataType == "Number"):
                print('Input should be a Number : ')
                if(textByUser.isnumeric() == True)  :  
                    print("Input is a Number")
                    mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                    print('Answer sent by USer : ' + textByUser)

                    nextQuestion += 1
                    if nextQuestion < 5 :
                        question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
                        print(question)
                        sendSessionMessage(question)
                else : 
                    sendSessionMessage('Incorrect Input....Input a Number')         
            else:
                print('Here')
                mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                print('Answer sent by User : ' + textByUser)

        else:
            sendSessionMessage('Thankyou for your Time !!')   

    elif(dataSent == 'audio'):
        print('Media is Audio')
        audio = data['data']
        print(audio)

        filename = audio.split("/")[-1].split("=")[-1]
        print(filename)

        nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
        print(nextQuestion)
        question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
        print(question)

        mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"audio_url":filename}}},upsert=True)
                   

    return "ok"             
