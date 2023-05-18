from bson import Binary

def read_image(file_path):
    with open(file_path, 'rb') as image_file:
        # Read the binary data of the image file
        image_data = image_file.read()
        # Convert the binary data into a BSON binary object
        bson_binary = Binary(image_data)
        return bson_binary
