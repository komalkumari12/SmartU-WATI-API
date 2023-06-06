from io import BytesIO
import requests
import json
import os
# import PyPDF2
import io
import base64

# import openai
from dotenv import load_dotenv
import os
load_dotenv()




def sendText(text, senderID):

    url = os.getenv("URL")+"/api/v1/sendSessionMessage/"+str(senderID)

    headers = {"Authorization": os.getenv("API")}

    body = {'messageText': text}

    response = requests.post(url, headers=headers, data=body)

    print(response.text)


def sendInteractiveButton(data, body_text, senderID):
    url = os.getenv("URL")+"/sendInteractiveButtonsMessage?whatsappNumber="+str(senderID)
    headers = {"content-type": "text/json",
               "Authorization": os.getenv("API")
               }
    body = {
        "body": body_text,  
        "buttons": data
    }

    response = requests.post(url, json=body, headers=headers)
    return response.status_code



def sendMedia(image_name, senderID):

    url = "https://live-server-101955.wati.io/api/v1/sendSessionFile/"+str(senderID)

    headers = {

        'Authorization': os.getenv("API"),
    }
    response = requests.get(image_name, headers=headers)

    if response.status_code == 200:
        file_data = response.content
        files = [('file', ('image.jpg', file_data, 'image/jpeg'))]
        headers = {'Authorization': os.getenv("API")}
        response = requests.post(url, headers=headers, files=files)
        return response.status_code
        # print(response.text)
    else:
        print(f'Error fetching image. Status code: {response}')




