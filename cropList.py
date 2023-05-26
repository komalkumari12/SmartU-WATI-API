import requests
from flask import request
# from deleteImageMongoDb import deleteImage

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def cropList():
    url = URL + "/sendInteractiveListMessage?whatsappNumber=918355882259"

    payload = {
        "header": "List of Variety Of  Crops",
        "body": "Choose one Crop",
        # "footer": "mc",
        "buttonText": "Crop",
        "sections": [
        {
            "title": "Crop",
            "rows": [
            {
                "title": "Crop1",
            },
            {
                "title": "Crop2",
            },
            {
                "title": "Crop3",
            },
            {
                "title": "Crop4",
            },
            {
                "title": "Crop5",
            },
            {
                "title": "Crop6",
            },
            {
                "title": "Crop7",
            },
            {
                "title": "Crop8",
            },
            {
                "title": "Crop9",
            },
            {
                "title": "Other",
            }
            ]
        }
  ]
}
    headers = {
        "content-type": "text/json",
        "Authorization": API
    }
    
    response = requests.post(url, json=payload, headers=headers)
    # print(response)
    # print(response.text)

    response_data = response.json()
    print(response_data)

    return "ok"