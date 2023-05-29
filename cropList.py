import requests
from flask import request
# from deleteImageMongoDb import deleteImage

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def cropListEnglish():
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
                "title": "Orange",
            },
            {
                "title": "Cotton",
            },
            {
                "title": "Wheat",
            },
            {
                "title": "Soybean",
            },
            {
                "title": "Gram",
            },
            {
                "title": "Onion",
            },
            {
                "title": "Banana",
            },
            {
                "title": "Groundnut",
            },
            {
                "title": "tur",
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


def cropListHindi():
    url = URL + "/sendInteractiveListMessage?whatsappNumber=918355882259"

    payload = {
        "header": "फसलों की किस्मों की सूची",
        "body": "एक फसल चुनें",
        # "footer": "mc",
        "buttonText": "काटना",
        "sections": [
        {
            "title": "काटना",
            "rows": [
            {
                "title": "सांता",
            },
            {
                "title": "कपास",
            },
            {
                "title": "गाह",
            },
            {
                "title": "सोयाबीन",
            },
            {
                "title": "ग्राम",
            },
            {
                "title": "प्याज",
            },
            {
                "title": "केला",
            },
            {
                "title": "मूंगफली",
            },
            {
                "title": "तूर",
            },
            {
                "title": "अन्य",
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

def cropListMarathi():
    url = URL + "/sendInteractiveListMessage?whatsappNumber=918355882259"

    payload = {
        "header": "पिकांच्या विविधतेची यादी",
        "body": "एक पीक निवडा",
        # "footer": "mc",
        "buttonText": "पीक",
        "sections": [
        {
            "title": "पीक",
            "rows": [
            {
                "title": "संता",
            },
            {
                "title": "कापूस",
            },
            {
                "title": "गह",
            },
            {
                "title": "सोयाबीन",
            },
            {
                "title": "हरभरा",
            },
            {
                "title": "कांदा",
            },
            {
                "title": "केळी",
            },
            {
                "title": "भुईमूग",
            },
            {
                "title": "तुर",
            },
            {
                "title": "इतर",
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
