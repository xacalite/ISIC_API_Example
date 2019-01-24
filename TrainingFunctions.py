
import os.path
import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.preprocessing.image import img_to_array, load_img

def TrainOnImagesInFolder(folderPath):
    encoding_dim = 32 # 32 floats
    input_img = keras.layers.Input(shape=(2351622,))
    encoded = keras.layers.Dense(encoding_dim, activation='relu')(input_img)
    decoded = keras.layers.Dense(2351622, activation='sigmoid')(encoded)
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
    trainingData = np.ndarray(shape=(len(train_files), image_height, image_width, channels),
                        dtype=np.float32)

    # Convert images from files to numpy arrays
    i = 0
    for _file in train_files:
        img = load_img(folderPath + "/" + _file)  # this is a PIL image
        img.thumbnail((image_width, image_height))
        # Convert to Numpy Array
        x = img_to_array(img)  
        trainingData[i] = x
        i += 1
        print("%d images to array" % i)

    # normalize input data
    trainingData = trainingData.astype('float32') / 255.
    trainingData = trainingData.reshape((len(trainingData), np.prod(trainingData.shape[1:])))
    print(trainingData.shape)

    # load saved weights if they exist; otherwise train and save
    save_path = "./Save/ISIC_training_weights"
    if os.path.isfile(save_path + ".index"):
        autoencoder.load_weights(save_path)
    else:
        # train the autoencoder
        autoencoder.fit(trainingData, trainingData,
                        epochs=2,
                        batch_size=10,
                        shuffle=True,
                        validation_split=(0.2))
        autoencoder.save_weights(save_path)