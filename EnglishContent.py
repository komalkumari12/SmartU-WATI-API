import mongoDB as mdb
from SessionMessage import sendSessionMessage
from cropList import cropListEnglish
from urllib.parse import urlparse
from  downloadAudio import downloadAudio
from MoreQuestions import moreQuestionsEnglish
from kcImage import execute,handleImageConfirmation

def EnglishContent0(nextQuestion):
    question = mdb.db2.English.find_one({"no":str(nextQuestion)})['question']
    print(question)
    sendSessionMessage(question)

def EnglishContent1():
    cropListEnglish()

    return "ok"

def EnglishContent2(data, textByUser):
    dataSent = data['type']

    print(dataSent)
    senderID = data.get('waId')

    nextQuestion = mdb.db['kc_upload'].find_one({'phoneNumber':918355882259})['next']
    print(nextQuestion)
    alreadyAsked = mdb.db['kc_upload'].find_one({'phoneNumber':918355882259})['already']
    print(alreadyAsked)   
    CropValue = mdb.db['kc_upload'].find_one({'phoneNumber':918355882259})['Crop Name']
    print("Crop Name is  : " + CropValue)

    if(dataSent == 'text'):
        print('Data sent is a text')
        print(nextQuestion)
        txt = data.get('text')
        if(txt == 'Ok'or txt == "होय" or txt =='सुधारित फोटो पाठवा' ):
            handleImageConfirmation(data)

        elif(nextQuestion < 5):
            print("Inside nextQuestion if Statement")
            question = mdb.db2.English.find_one({"no":str(nextQuestion)})['question']
            print(question)
            dataType = mdb.db2.English.find_one({"no":str(nextQuestion)})['dataType']
            print(dataType)

            # Store Response By Kc_upload
            if(dataType == "String"):
                print('Input should be a String : ')
                if(textByUser.isnumeric() == False)  :  
                    print("Input is a String")
                    if(alreadyAsked == 0):
                        print('Store value of Crop in a new field')
                        print('Text by Kc_upload is :  ' + textByUser)
                        mdb.db.kc_upload.update_one({'phoneNumber': 918355882259 },{'$set': {'Other': textByUser},"$inc":{"already":1,"next":1}},upsert=True)
                    # if(alreadyAsked == 1):
                    #     print('now add the acres as a seperate key value')
                    #     mdb.db.kc_upload.update_one({'phoneNumber': 918355882259 },{'$set': {'Acres': textByUser},"$inc":{"already":1,"next":1}},upsert=True)
                    else:
                        mdb.db.kc_upload.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                        print('Answer sent by Kc_upload : ' + textByUser)

                    nextQuestion += 1
                    if nextQuestion < 5 :
                        question = mdb.db2.English.find_one({"no":str(nextQuestion)})['question']
                        print(question)
                        sendSessionMessage(question)

                else : 
                    sendSessionMessage('Incorrect Input.... Input a string')
            elif(dataType == "Number"):
                print('Input should be a Number : ')
                if(textByUser.isnumeric() == True)  : 
                    print("Input is a Number")
                    textByUserNumber = int(textByUser)
                    # now check for range validation 
                    if(textByUserNumber < 100):

                        if(textByUserNumber >= 100 and alreadyAsked == 1):
                            print('Store value of Crop in a new field')
                            print('Text by Kc_upload is :  ' + textByUser)
                            mdb.db.kc_upload.update_one({'phoneNumber': 918355882259 },{'$set': {'Acre': textByUserNumber},"$inc":{"already":1,"next":1}},upsert=True)
                        else:
                            # user_data = {"phoneNumber":918355882259},{"$inc":{"already":1,"next":1}}
                            # update_parameters = {"$push":
                            # {"cropQuestions":{"Question":question,"Answer":textByUser}}
                            # }                                   
                            # mdb.db.kc_upload.update_one(user_data,update_parameters,upsert=True)
                            
                            mdb.db.kc_upload.update_one({"phoneNumber":918355882259},{"$inc":{"already":1,"next":1},"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)

                            print('Answer sent by Kc_upload : ' + textByUser)

                        nextQuestion += 1
                        if nextQuestion < 5 :
                            question = mdb.db2.English.find_one({"no":str(nextQuestion)})['question']
                            print(question)
                            sendSessionMessage(question)
                    else: 
                        sendSessionMessage('Number of Acres should be in Valid Range')
                else : 
                    sendSessionMessage('Incorrect Input.... Input a Number')         
            # else:
                # print('Input can be a string or Audio')
                # mdb.db.kc_upload.update_one({"phoneNumber":918355882259},{"$push":{"cropQuestions":{"Question":question,"Answer":textByUser}}},upsert=True)
                # print('Answer sent by Kc_upload : ' + textByUser)

    elif(dataSent == 'audio'):
        print('Media is Audio')
        audio = data['data']
        downloadAudio(audio)
        print(audio)
        nextQuestion = mdb.db['kc_upload'].find_one({'phoneNumber':918355882259})['next']
        print(nextQuestion)

        # length = len(mdb.db.kc_upload.find_one({'phoneNumber': 918355882259}).get('audio_urls', []))
        # print('Length of Audio Url is : ') 
        # print(length)

        mdb.db.kc_upload.update_one({'phoneNumber': 918355882259},{'$push': {'audio_urls': {'$each': [audio]}}},upsert=True)  
        
        moreQuestionsEnglish()

    elif(data['type']=='image'):
        print('image is sent by Kc_upload , Now in EnglishContent2 function')
        
    return "ok"             
