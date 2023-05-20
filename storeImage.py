import mongoDB
import base64
from readImage import read_image

# Read the image file as binary data
def store_image(phoneNumber, image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Convert the image binary data to a Base64-encoded string
    base64_image = base64.b64encode(image_data).decode('utf-8')
    # print(base64_image)

    # Insert the document with the Base64-encoded image string
    mongoDB.db.user.update_one({'phoneNumber': phoneNumber},{"$push": {"image": base64_image}})

    # Find the document with the Base64-encoded image string
    mongoDB.db.user.find({"image": base64_image})

    return base64_image    








# def store_image(phoneNumber, image_path):
#     # Read the image file and convert it to binary data
#     with open(image_path, 'rb') as image_file:
#         image_data = image_file.read()

#     # Update the document matching the phone number with the new image data
#     mongoDB.db.user.update_one(
#         {'phoneNumber': phoneNumber},
#         {"$push": {'image': image_data}}
#     )

#     print("Heyy I am trying  to access image url")
#     print(image_file)






