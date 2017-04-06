from keras.models import Sequential
from keras.layers.convolutional import Convolution2D
from keras.callbacks import ModelCheckpoint

import numpy as np
import os
from PIL import Image

BIT_DEPTH = 8
MAX_VAL = 2**8-1

TRAIN_PATH = "data/train/"
TRAIN_LABELS_PATH = "data/train_labels/"

def load_data(xPath, yPath):
    X, Y = [], []
    count = 0
    for file in os.listdir(xPath):
        if count > 100:
            break

        count += 1
        img = Image.open(xPath + file)
        imgArray = np.asarray(img, dtype='uint8')
        imgArray =  imgArray / (MAX_VAL * 1.0)
        X.append(imgArray)

        img = Image.open(yPath + file)
        imgArray = np.asarray(img, dtype='uint8')
        imgArray =  imgArray / (MAX_VAL * 1.0)
        Y.append(imgArray)

    return np.array(X), np.array(Y)


def get_model():
    model = Sequential()
    model.add(Convolution2D(32, 9, activation="relu", input_shape=(400,400,3), padding="same"))
    model.add(Convolution2D(16, 5, activation="relu", padding="same"))
    model.add(Convolution2D(3, 5, activation="relu", padding="same"))
    model.compile(optimizer="adam", loss="mse")

    return model


print ("start")
checkpointer = ModelCheckpoint(filepath="models/weights.hpytho5", verbose=1, save_best_only=True)
model = get_model()
print ("get model")
X,Y = load_data(TRAIN_PATH, TRAIN_LABELS_PATH)
print ("data loaded")
model.fit(X, Y, batch_size=32, epochs=1, validation_split=0.2, shuffle=True, callbacks=[checkpointer])
print ("fit done")
model.save('model.h5')