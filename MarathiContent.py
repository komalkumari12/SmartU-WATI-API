import mongoDB
from SessionMessage import sendSessionMessage
from cropList import cropList

def MarathiContent0(nextQuestion):
    question = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion)})['question']
    print(question)
    sendSessionMessage(question)

def MarathiContent1():
    cropList()

    return "ok"

def MarathiContent2(textByUser):
    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
    print(nextQuestion)   

    if(nextQuestion < 4):
        print("Inside nextQuestion if Statement")
        question = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion)})['question']
        print(question)
        dataType = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion)})['dataType']
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
                    question = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion)})['question']
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
                    question = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion)})['question']
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

    return "ok"

    result = mongoDB.db['user'].find_one({'phoneNumber':918355882259})
    print(result)

    print(textByUser)  
    print('In last block')
    nextQuestion = mongoDB.db['user'].find_one({'phoneNumber':918355882259})['next']
    print(nextQuestion)

    if(nextQuestion<=5):
        question = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion)})['question']
        print("question : "+ question)
        prevQuestion = mongoDB. db2.Marathi.find_one({"no" : str(nextQuestion-1)})['question']
        print("prevQuestion : " + prevQuestion)
        dataType = mongoDB.db2.Marathi.find_one({"no":str(nextQuestion-1)})['dataType']
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