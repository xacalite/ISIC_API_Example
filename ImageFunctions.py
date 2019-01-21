import requests
import json
import io
from PIL import Image

def DownloadAndShowImageByID(id):
    print ("Show image for " + id)
    urlString = 'https://isic-archive.com/api/v1/image/{}/download'.format(id)
    r2 = requests.get(urlString)
    imageBytes = r2._content
    image = Image.open(io.BytesIO(imageBytes))
    image.show()

def GetImagesFromISICArchive (numOfImagesToGet):
    r = requests.get('https://isic-archive.com/api/v1/image?limit=' + numOfImagesToGet + '&sort=name&sortdir=1&detail=false')
    listOfImages = r.json()
    return listOfImages

def Main():
    imageList = GetImagesFromISICArchive('1')
    for val in imageList:
        DownloadAndShowImageByID(val['_id'])

Main()