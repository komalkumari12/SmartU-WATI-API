import requests
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
load_dotenv()

def saveImageToCloudinary(image_url,senderID):
    
    name = image_url.split('/')[-1][:-4]
    payload = ""
    headers = {
    'Authorization': os.getenv('API'),
    'Cookie': 'affinity=1683959618.903.180936.971764|1656e65dbd355baa29fd80797f5ba486'
    }

    response = requests.request("GET", image_url, headers=headers, data=payload)
    with open("./sample.jpg", 'wb') as f:
        f.write(response.content)   
    
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))

    response = cloudinary.uploader.upload(
    "sample.jpg",
    public_id=name)
    
    print(response)
    
    return response['secure_url']
