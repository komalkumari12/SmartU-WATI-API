import requests
from dotenv import load_dotenv
import os 

load_dotenv()

API = os.getenv("API")
URL = os.getenv("URL")

def sendSessionMessage(msg):
    url = "https://live-server-101955.wati.io/api/v1/sendSessionMessage/918355882259"

    payload = {'messageText': str(msg)}
    files = []

    headers = {
        'Authorization': API,
        'Cookie': 'affinity=1682571857.622.180934.72523|1656e65dbd355baa29fd80797f5ba486'
    }
    
    print('In SessionMessage API')

    response = requests.post(url, headers=headers, data=payload, files=files)
    res = response.json()


    return res['message']['text']
