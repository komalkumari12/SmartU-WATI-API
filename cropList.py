import requests

from dotenv import load_dotenv
import os 
load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def cropList():
    url = URL + "/sendInteractiveButtonsMessage?whatsappNumber=918355882259"

    payload = {
        "buttons": [{"text": "option1"},{"text":"option2"},{"text":"other"}],
        "body": "Select One Option",
        "footer": ""
    }
    headers = {
        "content-type": "text/json",
        "Authorization": API
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    
    # print(response_data)
    user_response = ""

    print('Hello response')
    if response_data['ok']:
        message = response_data['message']
        print('Hello message')
        print(message)
        text = message['text']

        print(text)

        # if 'other' in text:
        #     user_response = "other"
        # elif 'option1' in text:
        #     print("User selected option1")
        #     user_response = "option1"
        # elif 'option2' in text:
        #     print("User selected option2")
        #     user_response = "option2"
        
        # elif 'option3' in text:
        #     print("User selected option3")
        #     user_response = "option3"
        # elif 'option4' in text:
        #     print("User selected option4")
        #     user_response = "option4"
        # elif 'option5' in text:
        #     print("User selected option5")
        #     user_response = "option5"
        # elif 'option6' in text:
        #     print("User selected option6")
        #     user_response = "option6"
        # elif 'option7' in text:
        #     print("User selected option7")
        #     user_response = "option7"
        # elif 'option8' in text:
        #     print("User selected option8")
        #     user_response = "option8"
        # elif 'option9' in text:
        #     print("User selected option9")
            # user_response = "option9"
        # else:
        #     print("Invalid selection")

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
