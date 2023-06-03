
from flask import Flask, request
import WATI as wa
# import airtable as at
from dotenv import load_dotenv
import re
import os
import time
from downloadImage import downloadImage
# import gdrive as gd
import mongoDB as mdb
# import redis_test as rd
load_dotenv()

app = Flask(__name__)
image_urls_arr = []


@app.route('/kc', methods=['POST', 'GET'])


def execute(data):
    data = request.json
    senderID = data['waId']
    name = data['senderName']

    print(data, type(senderID))
    """Check last message of airtable and send response"""

    # last_msg = at.get_field(senderID, "Last_Msg")
    last_msg = mdb.db['user'].find_one({'phoneNumber':918355882259})['user_id']
    print("last_msg ", last_msg)


# TODO: Add user_tag in MongoDB and validate using the same. 
# TODO: Add the following statement if data['type'] == 'image' and user_tag == "KC":
    
    if data['type'] == 'image':
        new_image_url = data.get('data')

# * MongoDB Operations

        # existing_record = mdb.find_user(senderID)
        existing_record = mdb.db['user'].find_one({'phoneNumber':918355882259})['phoneNumber']
        print(existing_record)
        """
        If existing_record is True, then update the image_url, stored_image and sent_image (0th index of image_url)
        else create a new record
        """
        if existing_record:
            print("1. existing_record ", existing_record)
            new_image_url = downloadImage(new_image_url)
            image_urls_arr.append(new_image_url)
            mdb.update_image_url(senderID, "image_url", new_image_url)
            mdb.update_image_url(senderID, "stored_image", new_image_url)
            image_urls = mdb.retrieve_field(senderID, "image_url")
            stored_image = mdb.retrieve_field(senderID, "stored_image")
            mdb.update_field_set(senderID, "sent_image", image_urls[0]) 
            
        else:
            print("2. does not have an existing_record ", existing_record)
            mdb.create_record(senderID, name, new_image_url)
            image_urls = mdb.retrieve_field(senderID, "image_url")
        
            
# TODO: Add the following statement if data['type'] == 'image' and user_tag == "KC":

    elif data.get("text") == "✔" and last_msg[1] == "KC" and last_msg != None:

        """
        Check if the last message is "KC Upload Invoked" and received text is ✔
        If true, then send the first image from the image_url array, update the sent_image field
        
        """
        user_exist = mdb.find_user(senderID)
        image_urls = mdb.retrieve_field(senderID, "image_url")
        stored_image = mdb.retrieve_field(senderID, "stored_image")

        print("user_exist", user_exist)
        # No image sent by the user
        if(stored_image == "No document found."):
            data = [{"text": "✔"}]
            media_response = wa.sendInteractiveButton(data, "No image received. Click on the button below after sending images.", senderID)

        else:
            # print("1. image_urls ", image_urls, "stored_image", stored_image)

            # print("2. image_urls ", image_urls[0])

            wa.sendMedia(image_urls[0], senderID)
            time.sleep(2)
            data = [{"text": "होय"}, {"text": "सुधारित फोटो पाठवा"}]
            media_response = wa.sendInteractiveButton(data, "Upload?", senderID)
            
            print("media_response", media_response)
            
            if media_response == 200:
                mdb.update_field_set(senderID, "sent_image", image_urls[0]) 

# TODO: Add the following statement if data['type'] == 'image' and user_tag == "KC":
    elif data.get("text") == "होय" :
        """
        Check if the received text is "होय"
        If true, 1. Upload the image to Google Drive
        2. Generate a public link
        
        """

        #Fetching the data from MongoDB
        image_urls = mdb.retrieve_field(senderID, "image_url")
        sent_image = mdb.retrieve_field(senderID, "sent_image")
        user_id = mdb.retrieve_field(senderID, "senderName")
        print("1. image_urls ", image_urls, "sent_image", sent_image)

        #* Upload to gdrive and airtable
        #TODO:(116,117) Replace with GD with Cloudinary code here

        print('Here I ahve to replace the code with cloudinary code')
        file_id = gd.upload_image_v2("filename.jpg", sent_image)
        public_link = gd.generate_public_link(file_id)

        at.upload(user_id[0],public_link)
        
        
        #* Removed image_url from array
        index_sent_image = image_urls.index(sent_image)
        print("index_sent_image", index_sent_image)
        image_urls.pop(index_sent_image)
        
        url_field_update = mdb.update_field_set(senderID, "image_url", image_urls) #Overwriting the image_url array by popping the sent_image_image url

        if(url_field_update == 200):
            print("After update ", image_urls)

            if(len(image_urls)>=2):
                wa.sendMedia(image_urls[index_sent_image+1], senderID)
                
                data = [{"text": "होय"}, {"text": "सुधारित फोटो पाठवा"}]
                media_response = wa.sendInteractiveButton(data, "Upload?", senderID)
                print("media_response", media_response)
                
                if media_response == 200:
                    mdb.update_field_set(senderID, "sent_image", image_urls[index_sent_image+1])
                    
            elif (len(image_urls) == 1):
                wa.sendMedia(image_urls[0], senderID)
                data = [{"text": "होय"}, {"text": "सुधारित फोटो पाठवा"}]
                media_response = wa.sendInteractiveButton(data, "Upload?", senderID)
                print("media_response", media_response)
                
                if media_response == 200:
                    mdb.update_field_set(senderID, "sent_image", image_urls[0])

            else:
                print("No more images to send")
                id = at.get_field(senderID, "Farmer Name")
                at.update_field(id[0], "Last_Msg", "Preview Completed")

                data = [{"text": "Yes"}, {"text": "नाही (पुढे जा)"}]

                media_response = wa.sendInteractiveButton(data, "आणखी फोटोस पाठवायचे आहे का?", senderID)
                print("media_response", media_response)
        

    elif data.get("text") == "सुधारित फोटो पाठवा":
        print("1. Inside सुधारित फोटो पाठवा")
        image_urls = mdb.retrieve_field(senderID, "image_url")
        stored_image = mdb.retrieve_field(senderID, "stored_image")
        sent_image = mdb.retrieve_field(senderID, "sent_image")

        print("1. image_urls ", image_urls, "stored_image", stored_image, "sent_image", sent_image)
        try:
                
            index_sent_image = image_urls.index(sent_image)
            index_stored_image = stored_image.index(sent_image)
        
            # print("2. index_sent_image", index_sent_image)
            # print("2. stored_image", stored_image)

            image_urls.pop(index_sent_image)
            stored_image.pop(index_stored_image)

            print("2. After removing image_urls ", len(image_urls))
            print("2. After removing stored_image ", len(stored_image))

            mdb.update_field_set(senderID, "image_url", image_urls)
            mdb.update_field_set(senderID, "stored_image", stored_image)

            # mdb.update_field_set(senderID, "sent_image", image_urls.len())

            data = [{"text": "✔"}]
            media_response = wa.sendInteractiveButton(data, "जुना फोटो हटवून नवीन अपलोड करा", senderID)
            
        except Exception as e:
            print("Exception", e)
    return data

if __name__ == '__main__':
    # from waitress import serve

    # serve(app, host="0.0.0.0", port=6000)
    app.run(threaded=True, debug=True, port=4000)


