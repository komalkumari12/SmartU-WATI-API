import requests
# from deleteImageMongoDb import deleteImage

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def sendInteractiveButtonMessage():
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "English"},{"text":"Hindi"},{"text":"Marathi"}],
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

# import requests
# import json

# def sendInteractiveButtonMessage():
#     url = "https://wati_api_endpoint/api/v1/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

#     payload = {
#         "buttons": [{"text": "English"}, {"text": "Hindi"}, {"text": "Marathi"}],
#         "body": "Languages"
#         }
#     headers = {
#         'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyNmQ3ZmNlNC1hOTVhLTRjMTgtYTg0YS03MmFkZjJmY2ZjOTciLCJ1bmlxdWVfbmFtZSI6InJhbXNoYXNoYWlraDc4MEBnbWFpbC5jb20iLCJuYW1laWQiOiJyYW1zaGFzaGFpa2g3ODBAZ21haWwuY29tIiwiZW1haWwiOiJyYW1zaGFzaGFpa2g3ODBAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDMvMjIvMjAyMyAwNToxNDozNyIsImRiX25hbWUiOiIxMDE5NTUiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.h0NlGLXpNb81R8alin1eBmFZ3aXjAZGSZKBGbXuUofY',
#         'Content-Type': 'application/json'
# }

#     response = requests.request("POST", url, headers=headers, data=payload)

#     print(response.text)

#     return "ok"
