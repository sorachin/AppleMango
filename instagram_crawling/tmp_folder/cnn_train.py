import os, re, glob
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

groups_folder_path = './cnn_sample/'
categories = ["ganjang-gejang","donkkaseu","doenjangjjigae","ramyeon","miyeoggug",
            "bossam","sundaegugbab","jogbal","jjajangmyeon","jjamppong","paseuta"]
num_classes = len(categories)

image_w = 28
image_h = 28
X = []
Y = []
  
for idex, categorie in enumerate(categories):
    label = [0 for i in range(num_classes)]
    label[idex] = 1
    image_dir = groups_folder_path + categorie + '/'
  
    for top, dir, f in os.walk(image_dir):
        for filename in f:
            # print(image_dir+filename)
            img = cv2.imread(image_dir+filename)
            img = cv2.resize(img, None, fx=image_w/img.shape[0], fy=image_h/img.shape[1])
            X.append(img/256)
            Y.append(label)
 
X = np.array(X)
Y = np.array(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y)
xy = (X_train, X_test, Y_train, Y_test)
np.save("./img_data.npy", xy)

print("==================================================================")
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Activation, Dense
from tensorflow.keras.layers import Flatten, Convolution2D, MaxPooling2D
from tensorflow.keras.models import load_model
import cv2
 
X_train, X_test, Y_train, Y_test = np.load('./img_data.npy')
 
model = Sequential()
model = Sequential()
model.add(Convolution2D(16, 3, 3, border_mode='same', activation='relu',
                        input_shape=X_train.shape[1:]))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
  
model.add(Convolution2D(64, 3, 3,  activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
 
model.add(Convolution2D(64, 3, 3))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
  
model.add(Flatten())
model.add(Dense(256, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes,activation = 'softmax'))
  
model.compile(loss='binary_crossentropy',optimizer='Adam',metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=32, nb_epoch=100)
 
model.save('Gersang.h5')

X_train = np.append(X_train,X_test, axis=0)
Y_train = np.append(Y_train,Y_test, axis=0)
 
# # Save Model with CheckPoint & StopPoint
# from keras.callbacks import ModelCheckpoint,EarlyStopping
# import os
# import datetime
 
# Datetime = datetime.datetime.now().strftime('%m%d_%H%M')
# modelpath="Gersang.h5"
 
# checkpointer = ModelCheckpoint(filepath=modelpath, monitor='loss', verbose=1, save_best_only=True)
# early_stopping_callback = EarlyStopping(monitor='loss', patience=100)
 
# # Learning and save models
# model.fit(X_train, Y_train, validation_split=0.1, epochs=3500, batch_size=10, verbose=0, callbacks=[early_stopping_callback,checkpointer])


