import requests
import json
import io
import os.path
from PIL import Image

def GetImageListFromISICArchive (numOfImagesToGet):
    r = requests.get('https://isic-archive.com/api/v1/image?limit=' + numOfImagesToGet + '&sort=name&sortdir=1&detail=false')
    listOfImages = r.json()
    return listOfImages

def GetImageByID(id):
    print ("Show image for " + id)
    urlString = 'https://isic-archive.com/api/v1/image/{}/download'.format(id)
    r2 = requests.get(urlString)
    imageBytes = r2._content
    image = Image.open(io.BytesIO(imageBytes))
    return image 

def CheckFolder():
    folder = os.getcwd() + "/Images/"
    folderExists = os.path.isdir(folder)
    if (not folderExists):
        os.mkdir(folder)
    return folder

def Main():
    numberOfImagesToGet = '3'
    try:
        imageList = GetImageListFromISICArchive(numberOfImagesToGet)
    except:
        print ("Unable to connect to ISIC Archive; ending program")
        return

    # if connection to ISIC archive has been successful, then
    for val in imageList:
        extension = '.jpg'
        path = CheckFolder() + val['name'] + extension
        alreadyExists = os.path.isfile(path)
        if alreadyExists:
            print('File already exists at ' + path)
            continue
        else:
            print ('Download and save file to ' + path)
            image = GetImageByID(val['_id'])
            image.save(path)

Main()