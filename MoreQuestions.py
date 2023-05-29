import requests
# from deleteImageMongoDb import deleteImage

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def moreQuestions():
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "Yes"},{"text":"No"}],
        "body": "Do you want to add more questions ??",
        "footer": ""
    }
    headers = {
        "content-type": "text/json",
        "Authorization": API
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    print(response_data)
    user_response = ""

    if response_data['ok']:
        message = response_data['message']
        text = message['text']

        if 'Yes' in text:
            print("User selected Yes")
            user_response = "Yes"
        elif 'No' in text:
            print("User selected No")
            user_response = "No"
        else:
            print("Invalid selection")

    return user_response
