import mongoDB
from SessionMessage import sendSessionMessage


def HindiContent1(textByUser, senderName):
    mongoDB.db.user.insert_one({"phoneNumber":918355882259, "senderName": senderName,"language": textByUser,"already":0,"next":1}) 

    language = mongoDB.db.user.find_one({"phoneNumber" : 918355882259, "senderName": senderName,"language": textByUser,})['language']
    print(language)

    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
    print(nextQuestion)
    question = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion)})['question']
    print(question)
    sendSessionMessage(question)
    mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":question,"A":textByUser}}},upsert=True)


def HindiContent2(textByUser):
    print(textByUser)  
    print('In last block')
    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']

    if(nextQuestion<=4):
        question = mongoDB.db2.Hindi.find_one({"no":str(nextQuestion)})['question']
        prevQuestion = mongoDB. db2.Hindi.find_one({"no" : str(nextQuestion-1)})['question']

        sendSessionMessage(question)
        mongoDB.db.user.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"questionsAsked":{"Q":prevQuestion,"A":textByUser}}},upsert=True)
    else : 
        sendSessionMessage("Thankyou For Your Time !!")