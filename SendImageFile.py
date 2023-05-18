import requests
# from deleteImageMongoDb import deleteImage

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def sendImageFile(img, data):
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
    
    # print("Hello1")
    response = requests.post(url, json=payload, headers=headers)

    return "Done"

    #Checking the response of User
    # data = request.json
    # print("Hello 2")
    # user_response = data['actions'][0]['text']
    # print('User response:', user_response)
    
    # print("Helloo3")

    # # Process the user's response
    # if user_response.lower() == 'no':
    # # User clicked "No" button
    # # Delete the image from cloudinary and mongoDB both
    #     print("User input is a No")
    #     print("Yeahhhhh")
    #     # deleteImageMongoDb()
    #     pass
    
    

