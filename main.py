import cv2
import os
import urllib.request
import numpy as np
from config import *
from lxml import etree
from random import randint
from telethon import TelegramClient, events, sync
from telethon.tl.functions.photos import UploadProfilePhotoRequest

### Log in Telegram

try:
    proxy
except NameError:
    proxy = None

print('Logging in Telegram')

client = TelegramClient('waifu_session', api_id, api_hash, proxy=proxy)
client.start()

print('Logged in as', client.get_me().username)

### Download image list

data = urllib.request.urlopen(search_url).read()
html = etree.HTML(data)
image_detail_urls = html.xpath("//ul[@id='post-list-posts']/li[count(a/span[2][substring-before(text() , 'x') >= substring-after(text() , 'x')]) > 0]//a[@class='thumb']/@href")
count = len(image_detail_urls)
print('Got', count, 'images')

### Face detection

def detect(image, cascade_file=cascade_file):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (100, 100))
    return faces

### Download image

for _ in range(count):
    image_detail_url = url_prefix + image_detail_urls[randint(0, count - 1)]
    image_detail = urllib.request.urlopen(image_detail_url).read()
    html = etree.HTML(image_detail)
    image_url = html.xpath("//*[@id='highres']/@href")[0]
    print('Image URL:', image_url)
    image_data = urllib.request.urlopen(image_url).read()
    arr = np.asarray(bytearray(image_data), dtype=np.uint8)
    # Detect face
    img = cv2.imdecode(arr, -1)
    faces = detect(img)
    if len(faces) == 0:
        print('No face detected')
        continue
    if len(faces) > 1:
        print('Too many faces:', len(faces))
        continue
    print('Detected', len(faces), 'faces')
    face = faces[randint(0, len(faces) - 1)]
    (x, y, w, h) = face
    crop_img = img[y:y+h, x:x+w]
    encoded = cv2.imencode('.png', crop_img)[1]
    data_encoded = np.array(encoded)
    str_encoded = data_encoded.tostring()
    print(len(str_encoded))

### Set profile photo

    # uploaded = client.upload_file(str_encoded)
    # print('Uploaded ID:', uploaded.id)
    # client(UploadProfilePhotoRequest(uploaded))
    # print('Successfully changed profile photo')

### Log
    with open('avatar.log', 'w+') as f:
        f.write(image_detail_url + '\n')
    break
