import requests
# from deleteImageMongoDb import deleteImage

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def moreQuestionsEnglish():
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "Yes"},{"text":"No"}],
        "body": "Do you want to add more queries ??",
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

def moreQuestionsHindi():
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "हाँ"},{"text":"नहीं"}],
        "body": "क्या आप और प्रश्न जोड़ना चाहेंगे?",
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

def moreQuestionsMarathi():
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "होय"},{"text":"नाही"}],
        "body": "आपल्याकडे अधिक प्रश्न जोडायला आहे का?",
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
