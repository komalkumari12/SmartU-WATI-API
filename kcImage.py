
from flask import Flask, request
import WATI as wa
from dotenv import load_dotenv
import re
import os
import time
import utils
import mongoDB as mdb
load_dotenv()

app = Flask(__name__)
image_urls_arr = []


@app.route('/sendMessage', methods=['POST', 'GET'])


def handleImageConfirmation(data):
    if data.get("text") == "Ok":
        """
        Check if the last message is "KC Upload Invoked" and received text is Ok
        If true, then send the first image from the image_url array, update the sent_image field
        
        """
        user_exist = mdb.find_user(918355882259)
        image_urls = mdb.retrieve_field(918355882259, "image_url")
        stored_image = mdb.retrieve_field(918355882259, "stored_image")

        # print("user_exist", user_exist)
        # No image sent by the user
        if(stored_image == "No document found."):
            data = [{"text": "Ok"}]
            media_response = wa.sendInteractiveButton(data, "No image received. Click on the button below after sending images.", 918355882259)

        else:
            # print("1. image_urls ", image_urls, "stored_image", stored_image)

            # print("2. image_urls ", image_urls[0])
            
            wa.sendMedia(image_urls[0], 918355882259)
            time.sleep(2)
            data = [{"text": "होय"}, {"text": "सुधारित फोटो पाठवा"}]
            media_response = wa.sendInteractiveButton(data, "Upload?", 918355882259)
            
            # print("media_response", media_response)
            
            if media_response == 200:
                mdb.update_field_set(918355882259, "sent_image", image_urls[0]) 

# TODO: Add the following statement if data['type'] == 'image' and user_tag == "KC":
    elif data.get("text") == "होय" :
        """
        Check if the received text is "होय"
        If true, 1. Upload the image to Google Drive
        2. Generate a public link
        
        """

        #Fetching the data from MongoDB
        image_urls = mdb.retrieve_field(918355882259, "image_url")
        sent_image = mdb.retrieve_field(918355882259, "sent_image")
        # user_id = at.get_field(918355882259, "Farmer senderName")
        # print("1. image_urls ", image_urls, "sent_image", sent_image)

        #* Upload to gdrive and airtable
        #TODO:(116,117) Replace with GD with Cloudinary code here
        public_link = utils.saveImageToCloudinary(sent_image,918355882259)
        # print(public_link)
        # file_id = gd.upload_image_v2("filename.jpg", sent_image)
        # public_link = gd.generate_public_link(file_id)
        mdb.update_cloudinary_images(918355882259,'cloudinary_images',public_link)
        # at.upload(user_id[0],public_link)
        
        print("destiny",len(image_urls),sent_image)

        #* Removed image_url from array
        index_sent_image = image_urls.index(sent_image)
        # print("index_sent_image", index_sent_image)
        image_urls.pop(index_sent_image)
        
        url_field_update = mdb.update_field_set(918355882259, "image_url", image_urls) #Overwriting the image_url array by popping the sent_image_image url
        print("destiny",len(image_urls),index_sent_image)
        if(url_field_update == 200):
            
            if(len(image_urls)>2):
                wa.sendMedia(image_urls[index_sent_image+1], 918355882259)
                
                data = [{"text": "होय"}, {"text": "सुधारित फोटो पाठवा"}]
                media_response = wa.sendInteractiveButton(data, "Upload?", 918355882259)
                # print("media_response", media_response)
                
                if media_response == 200:
                    mdb.update_field_set(918355882259, "sent_image", image_urls[index_sent_image+1])
            elif(len(image_urls)==2):
                wa.sendMedia(image_urls[index_sent_image], 918355882259)
                
                data = [{"text": "होय"}, {"text": "सुधारित फोटो पाठवा"}]
                media_response = wa.sendInteractiveButton(data, "Upload?", 918355882259)
                # print("media_response", media_response)
                
                if media_response == 200:
                    mdb.update_field_set(918355882259, "sent_image", image_urls[index_sent_image])
            
            elif (len(image_urls) == 1):
                wa.sendMedia(image_urls[0], 918355882259)
                data = [{"text": "होय"}, {"text": "सुधारित फोटो पाठवा"}]
                media_response = wa.sendInteractiveButton(data, "Upload?", 918355882259)
                # print("media_response", media_response)
                
                if media_response == 200:
                    mdb.update_field_set(918355882259, "sent_image", image_urls[0])

            else:
                print("No more images to send")
                # id = at.get_field(918355882259, "Farmer senderName")
                # at.update_field(id[0], "Last_Msg", "Preview Completed")

                data = [{"text": "Yess"}, {"text": "नाही (पुढे जा)"}]

                media_response = wa.sendInteractiveButton(data, "आणखी फोटोस पाठवायचे आहे का?", 918355882259)
                # print("media_response", media_response)
        

    elif data.get("text") == "सुधारित फोटो पाठवा":
        print("1. Inside सुधारित फोटो पाठवा")
        image_urls = mdb.retrieve_field(918355882259, "image_url")
        stored_image = mdb.retrieve_field(918355882259, "stored_image")
        sent_image = mdb.retrieve_field(918355882259, "sent_image")

        # print("1. image_urls ", image_urls, "stored_image", stored_image, "sent_image", sent_image)
        try:
                
            index_sent_image = image_urls.index(sent_image)
            index_stored_image = stored_image.index(sent_image)
        
            # print("2. index_sent_image", index_sent_image)
            # print("2. stored_image", stored_image)

            image_urls.pop(index_sent_image)
            stored_image.pop(index_stored_image)

            # print("2. After removing image_urls ", len(image_urls))
            # print("2. After removing stored_image ", len(stored_image))

            mdb.update_field_set(918355882259, "image_url", image_urls)
            mdb.update_field_set(918355882259, "stored_image", stored_image)

            # mdb.update_field_set(918355882259, "sent_image", image_urls.len())

            data = [{"text": "Ok"}]
            media_response = wa.sendInteractiveButton(data, "जुना फोटो हटवून नवीन अपलोड करा", 918355882259)
            
        except Exception as e:
            print("Exception", e)
    


def execute(data):
    data = request.json
    
    senderName = data['senderName']
    phoneNumber = data['waId']

    print(data, type(918355882259))
    """Check last message of airtable and send response"""

    last_msg = mdb.find_user(918355882259)
    print("last_msg ", last_msg)


# # TODO: Add user_tag in MongoDB and validate using the same. 
# # TODO: Add the following statement if data['type'] == 'image' and user_tag == "KC":
    
    if data['type'] == 'image':
        new_image_url = data.get('data')

# * MongoDB Operations
        # print(data)
        existing_record = mdb.find_user(918355882259)
        # print(existing_record)

        """
        If existing_record is True, then update the image_url, stored_image and sent_image (0th index of image_url)
        else create a new record
        """
        if existing_record:
            # print("1. existing_record ", existing_record)

            mdb.update_image_url(918355882259, "image_url", new_image_url)
            mdb.update_image_url(918355882259, "stored_image", new_image_url)
            image_urls = mdb.retrieve_field(918355882259, "image_url")
            stored_image = mdb.retrieve_field(918355882259, "stored_image")
            mdb.update_field_set(918355882259, "sent_image", image_urls[0]) 
            # print("image testing ",image_urls)
        else:
            print("2. does not have an existing_record ", existing_record)
            mdb.create_record(918355882259, senderName, new_image_url)
            image_urls = mdb.retrieve_field(918355882259, "image_url")
        
            
# TODO: Add the following statement if data['type'] == 'image' and user_tag == "KC":
        return "ok"
