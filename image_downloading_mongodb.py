import requests
from pymongo import MongoClient
import gridfs

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")


def store_image_in_mongodb(image_data, image_name, db_name='images', collection_name='img'):
    client = MongoClient('mongodb://localhost')
    db = client[db_name]
    fs = gridfs.GridFS(db, collection=collection_name)
    file_id = fs.put(image_data, filename=image_name)
    return file_id


if __name__ == "__main__":
    image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfcMkNiLDXVaULaetBzC3xD2HDLaDRmvSKsw&s'
    image_name = 'image.jpg'

    try:
        image_data = download_image(image_url)
        file_id = store_image_in_mongodb(image_data, image_name)
        print(f"Image stored in MongoDB with file ID: {file_id}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
