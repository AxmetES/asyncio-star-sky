def get_image(file_name):
    with open(file_name, 'r') as file:
        image_content = file.read()
    return image_content
