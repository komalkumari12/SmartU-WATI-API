import requests

from dotenv import load_dotenv
import os 
load_dotenv()

# API = os.getenv("API")
# URL = os.getenv("URL")

def sendImageFile():
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "sdfsdfsdf"}],
        "header": {
            "media": {
                "fileName": "Image",
                "url": "https://images.pexels.com/photos/617278/pexels-photo-617278.jpeg?auto=compress&cs=tinysrgb&w=600"
            },
            "text": "sdf",
            "type": "Image"
        },
        "body": "Cat Image",
        "footer": "from google"
    }
    headers = {
        "content-type": "text/json",
        "Authorization": API
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

