import mongoDB
from bson import Binary

# def deleteImage(): 
#     image_data = b'\x00\x01\x02...'  # Replace with the actual binary image data you want to delete
#     query = {'image': {'$in': [Binary(image_data)]}}
#     update = {'$pull': {'image': {'$in': [Binary(image_data)]}}}
#     result = mongoDB.db.user.update_many(query, update)

#     if result.modified_count > 0:
#         print('Image deleted successfully.')
#     else:
#         print('Image not found or could not be deleted.')



def retrieve_image():
    image_doc = mongoDB.db.user.find_one()
    # Get the file ID from the document
    file_id = image_doc['image']
    # Retrieve the image file from GridFS
    image_file = fs.get(file_id)
    # Save the image file to disk
    with open('retrieved_image.jpg', 'wb') as output_file:
        output_file.write(image_file.read())
