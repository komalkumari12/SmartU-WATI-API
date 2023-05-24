import mongoDB
from validate_Input import validate_string_input
from SessionMessage import sendSessionMessage

def EnglishContent1(textByUser, senderName):
    result = mongoDB.db['user'].find_one({'phoneNumber':918355882259})
    print(result)
    
    # if(result):
    #     print('User not created')

    if(result == 'None'):
        print('User created for the first Time')
        mongoDB.db.user.update_one({"phoneNumber": 918355882259},{"$set": {"language": textByUser}},upsert=True)
    else:
        print('Language updated')
        print('updated language should be' + textByUser)
        mongoDB.db.user.insert_one({"phoneNumber":918355882259, "senderName": senderName,"language": textByUser,"already":0,"next":1}) 

    language = mongoDB.db.user.find_one({"phoneNumber" : 918355882259, "senderName": senderName,"language": textByUser,})['language']
    print(language)

    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
    print(nextQuestion)
    question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
    print(question)
    
    
    sendSessionMessage(question)
    mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":question,"A":textByUser}}},upsert=True)


def EnglishContent2(textByUser):
    result = mongoDB.db['user'].find_one({'phoneNumber':918355882259})
    print(result)

    print(textByUser)  
    print('In last block')
    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
    print(nextQuestion)

    if(nextQuestion<=5):
        question = mongoDB.db2.English.find_one({"no":str(nextQuestion)})['question']
        print("question : "+ question)
        prevQuestion = mongoDB. db2.English.find_one({"no" : str(nextQuestion-1)})['question']
        print("prevQuestion : " + prevQuestion)
        dataType = mongoDB.db2.English.find_one({"no":str(nextQuestion-1)})['dataType']
        print(dataType)


        if(dataType == 'String'):
            print('Input should be a String : ')
            # if validate_string_input(textByUser):
            if(textByUser.isnumeric() == False)  :  
                print("Input is a String")
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
        sendSessionMessage("All Questions are completed !!")
