import requests
# from deleteImageMongoDb import deleteImage

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def languagePreference():
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "English"},{"text":"हिंदी"},{"text":"मराठी"}],
        "body": "Language?",
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

        if 'English' in text:
            print("User selected English")
            user_response = "English"
        elif 'Hindi' in text:
            print("User selected Hindi")
            user_response = "Hindi"
        elif 'Marathi' in text:
            print("User selected Marathi")
            user_response = "Marathi"
        else:
            print("Invalid selection")

    return user_response