import requests
import json
import io
import os.path
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.preprocessing.image import img_to_array, load_img

def GetImageListFromISICArchive (numOfImagesToGet):
    r = requests.get('https://isic-archive.com/api/v1/image?limit=' + numOfImagesToGet + '&sort=name&sortdir=1&detail=false')
    listOfImages = r.json()
    return listOfImages

def GetImageByID(id):
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

def DoTraining(folderPath):
    encoding_dim = 32 # 32 floats
    input_img = keras.layers.Input(shape=(784,))
    encoded = keras.layers.Dense(encoding_dim, activation='relu')(input_img)
    decoded = keras.layers.Dense(784, activation='sigmoid')(encoded)
    autoencoder = keras.models.Model(input_img, decoded)
    encoder = keras.models.Model(input_img, encoded)
    encoded_input = keras.layers.Input(shape=(encoding_dim,))
    decoder_layer = autoencoder.layers[-1]
    decoder = keras.models.Model(encoded_input, decoder_layer(encoded_input))
    autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
    
    # load dataset
    onlyfiles = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]
    print("Working with {0} images".format(len(onlyfiles)))

    train_files = []
    y_train = []
    
    for _file in onlyfiles:
        train_files.append(_file)
        #label_in_file = _file.find("_")
        #y_train.append(int(_file[0:label_in_file]))
        
    print("Files in train_files: %d" % len(train_files))
    

    # Original Dimensions
    image_width = 1022
    image_height = 767
    channels = 3

    # Create placeholder for image set
    x_train = np.ndarray(shape=(len(train_files), image_height, image_width, channels),
                        dtype=np.float32)

    # Convert images from files to numpy arrays
    i = 0
    for _file in train_files:
        img = load_img(folderPath + "/" + _file)  # this is a PIL image
        img.thumbnail((image_width, image_height))
        # Convert to Numpy Array
        x = img_to_array(img)  
        x_train[i] = x
        i += 1
        print("%d images to array" % i)

    # normalize input data
    x_train = x_train.astype('float32') / 255.
    #x_test = x_test.astype('float32') / 255.
    x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
    #x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
    print(x_train.shape)
    #print(x_test.shape)

def main():
    numberOfImagesToGet = '10'
    try:
        imageList = GetImageListFromISICArchive(numberOfImagesToGet)
    except:
        print ("Unable to connect to ISIC Archive; ending program")
        return

    folderPath = CheckFolder()
    # if connection to ISIC archive has been successful, then
    for val in imageList:
        extension = '.jpg'
        path = folderPath + val['name'] + extension
        alreadyExists = os.path.isfile(path)
        if alreadyExists:
            print('File already exists at ' + path)
            continue
        else:
            print ('Download and save file to ' + path)
            image = GetImageByID(val['_id'])
            image.save(path)
    print (val)


    DoTraining(folderPath)

if __name__ == '__main__':
    main()