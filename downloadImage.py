import requests
import cloudinary
import cloudinary.uploader
import os


def downloadImage(url):
    payload = ""
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyNmQ3ZmNlNC1hOTVhLTRjMTgtYTg0YS03MmFkZjJmY2ZjOTciLCJ1bmlxdWVfbmFtZSI6InJhbXNoYXNoYWlraDc4MEBnbWFpbC5jb20iLCJuYW1laWQiOiJyYW1zaGFzaGFpa2g3ODBAZ21haWwuY29tIiwiZW1haWwiOiJyYW1zaGFzaGFpa2g3ODBAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDMvMjIvMjAyMyAwNToxNDozNyIsImRiX25hbWUiOiIxMDE5NTUiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.h0NlGLXpNb81R8alin1eBmFZ3aXjAZGSZKBGbXuUofY',
    'Cookie': 'affinity=1683959618.903.180936.971764|1656e65dbd355baa29fd80797f5ba486'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    with open("./sample.jpg", 'wb') as f:
        f.write(response.content)   
    
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))

    response = cloudinary.uploader.upload(
    "sample.jpg",
    public_id="my_uploaded_image"
)
    
    return response['secure_url']
