import requests
# from deleteImageMongoDb import deleteImage

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def sendImageFile(img):
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "Yes"},{"text":"No"}],
        "header": {
            "media": {
                "fileName": "Image",
                "url": img
            },
            "text": "Are You Sure",
            "type": "Image"
        },
        "body": "Are You sure you want to send this image?",
        "footer": ""
    }
    headers = {
        "content-type": "text/json",
        "Authorization": API
    }
    
    response = requests.post(url, json=payload, headers=headers)

    return "Done"

