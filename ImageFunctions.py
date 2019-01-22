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

def SaveImageToFile(image, fileName):
    extension = '.jpg'
    path = CheckFolder() + fileName + extension
    alreadyExists = os.path.isfile(path)
    if alreadyExists:
        print('File already exists at ' + path)
        return
    else:
        print ('Save file to ' + path)
        image.save(path)

def CheckFolder():
    folder = os.getcwd() + "\Images\\"
    folderExists = os.path.isdir(folder)
    if (folderExists):
        print ("Folder " + folder + " already exists")
    else:
        print ("Creating folder " + folder)
        os.mkdir(folder)
    return folder

def Main():
    imageList = GetImageListFromISICArchive('1')
    for val in imageList:
        image = GetImageByID(val['_id'])
        SaveImageToFile(image, val['name'])
        #image.show()
Main()