import piexif
from PIL import Image
from io import BytesIO
import requests
import json

from requests.api import post

def open_image(PATH="test.jpg", url=None):

    try:
        
        try:

            response = requests.get(url)
            img_bytes = BytesIO(response.content)
            img = Image.open(img_bytes)

        except requests.exceptions.RequestException:   

            img = Image.open(PATH)

        if 'exif' in img.info:

            exif = piexif.load(img.info['exif'])
            
        else:
            exif = None
        dict = {
                str(PATH):str(exif)
                }
        return img, dict
    except requests.exceptions.RequestException:
        print('Error loading image data') 



def write_json(data, filename='data.json'):
    with open(filename,'r+') as file:
       
        file_data = json.load(file)
    
        file_data["emp_details"].append(data)
    
        file.seek(0)
    
        json.dump(file_data, file, indent = 4)
    
    


def remove_exif(img):
    piexif.remove(img)
    newdata = {'0th': {271: b'In case of an investigation by any federal entity or similar, I do not have any involvement with this group or with the people in it, I do not know how I am here, probably added by a thrid party, I do not support any actions by the member of this group.'}}
    exif_bytes = piexif.dump(newdata)
    piexif.insert(exif_bytes, img)
    return img

def post_data(file):
    url = ''

    headers = {
    'Content-Type': 'application/json',
    'X-Master-Key': ''
    }
    
    
    req = requests.post(url, json=file, headers=headers)
    print(req.text)

def modify(PATH):

    img, dict = open_image(PATH)

    r = write_json(dict, 'data.json')
    img = remove_exif(PATH)
    print('EXIF data removal complete')
    #post_data(dict)

    return img

modify('IMG_2452.jpg')
