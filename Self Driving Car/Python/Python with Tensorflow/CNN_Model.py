
import pandas as p
import cv2
from sklearn import model_selection

import tensorflow as tf
from tensorflow.keras.models import Sequential#, Input
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Lambda, Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint

from PIL import Image
import numpy as np

image_input_array = []

def LoadData():  
    image_input_array2 = np.zeros((4536, 66, 200,3))         # Replace the value of 2116 with the number of images, you are going to train.
    URL = r"D:\ML\Unity-ML\sdcdata_1.csv"		        # Load your csv file.
    url_image = r"D:\\ML\\Unity-ML\\SDC\\"
    
    data = p.read_csv(URL)
    
    image_input = data['Image Directory']
    steering_Angle = data['Steering Angle'].values
    
    for i in range(0,len(image_input)):
        #print("Proccessing image: ", i)
        
        URL_image = image_input[i]
        #print(URL_image)
        # addd path to variable URL_image
        image_input_array = Image.open(url_image +URL_image)
        image_input_list = np.array(image_input_array)         
        #print(image_input_list.shape)           
        
        image_input_list2 = cv2.resize(image_input_list, dsize=(200, 66), interpolation=cv2.INTER_CUBIC)
        #print(image_input_list2.shape)
        
        image_input_list2 = np.expand_dims(image_input_list2, axis=0)
        #print(image_input_list2.shape)      
        #print(len(image_input_list2))
        
        image_input_array2[i, :, :, :] = image_input_list2
        #print(image_input_array2.shape)
        #print(len(image_input_array2))
        #image_input_list2.show()
        
        if i % 100 == 0:
            print("\r", end='')
            print("Image Processed: ", i,end = '', flush = False)
    
    #print(image_input_array.)
    print("Processng image Done!")
    print(image_input_array2.shape)
    #image_input_array2 = np.array(image_input_array3)
    #image_input_list = np.expand_dims(image_input_list, axis=0)
    '''
    print(image_input_list.shape)
    
    for i in range(0,10):
        image_input_array2[i,:,:,:] = image_input_list
    '''    
    #split(image_input)
        
    #image_input_list.resize((2116,420,750,3))
  
    '''
    arrs = [np.random.random((420, 750, 3))
        for i in range(len(image_input_list))]

    image_input_list = np.array(arrs)
    
    new_image = np.ones((1,420,750,3))    
    # lets jsut say you have two Images 
    old_image = np.reshape(image_input_list , (1,420,750,3))
    new_image = np.reshape(new_image , (2115,420,750,3))
    image_input_list = np.append( new_image , old_image , axis = 0)
    '''
    
    #print(image_input_list.shape)
    #print(len(image_input_list))
    
    validation_size = 0.15          # validation is 0.20, so the size of the X and Y validaion will be 20% of the X and Y(actual size of the array)
    seed = 7
    
    #image_input_list = image_input_list.reshape(1, 420, 750, 3, )
    #print("size is: ",image_input_list.shape)
    
    # This splits the dataset, so that we can use some data for training, some for testing.
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(image_input_array2, steering_Angle, test_size=validation_size, random_state=seed)
    
    '''
    for i in range(0,1693): # 0, 1693
        print("Proccessing X_train image: ", i)
        URL_image = image_input[i]
        image_input_array = PImage.open(URL_image)
        X_train = np.array(image_input_array)  
        
        Y_train = data[' Steerring Angle'].values
          
        #print(X_train.shape)           # 420, 750, 3
        #print(Y_train.shape)
        
        #print(len(X_train))
        #image_input_array.show()

    for i in range(1693,len(image_input)): #1693, length
        print("Proccessing X_validation image: ", i)
        URL_image = image_input[i]
        image_input_array = PImage.open(URL_image)
        X_validation = np.array(image_input_array) 
        
        Y_validation = data[' Steerring Angle'].values
        
        #print(X_validation.shape)           # 420, 750, 3
        #print(Y_validation.shape)
        
        #print(len(X_validation))
        #mage_input_array.show()
    '''
  				 # If the actual image and steering data is 2116, then...    
    print(X_train.shape)         # the Size is 1692 which is about 80% of actual image data.         1692/2116 * 100 = 79.9621% ~ 80%
    print(Y_train.shape)         # the size is 1692 which is about 80% of actual steering data.      1692/2116 * 100 = 79.9621% ~ 80%
    print(X_validation.shape)    # the size is 424 which is about 20% of actual image data.          424/2116 * 100 = 20.0378% ~ 20%
    print(Y_validation.shape)    # the size is 424 which is about 20% of actual steering data.       424/2116 * 100 = 20.0378% ~ 20%
    
    return X_train, X_validation, Y_train, Y_validation

def buildModel(image_train):
    #print("building our model")
    model = Sequential()
    model.add(Lambda(lambda x : x/127.5-1.0, input_shape = (66,200,3) ))
    model.add(Conv2D(24, (5, 5), activation = "elu", strides=(2,2)))
    model.add(Conv2D(36, (5, 5), activation = "elu", strides=(2,2)))
    model.add(Conv2D(48, (5, 5), activation = "elu", strides=(2,2)))
    model.add(Conv2D(64, (5, 5), activation = "elu"))
    #model.add(Conv2D(64, (5, 5), activation = "elu"))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1, activation='elu'))
    model.summary()
    
    return model

def train(model, image_train, image_valiation, steer_train, steer_validation):
    checkpoints = ModelCheckpoint('data-{epoch:03d}.h5', monitor='val_loss', verbose=0, save_best_only=True, mode='auto')    # You can change the name of the model, by replacing "data" with your preferred name.
    
    model.compile(loss='mean_squared_error', optimizer=Adam(lr = 0.001))
    
    model.fit(image_train, steer_train, epochs=60, callbacks=[checkpoints],validation_data=(image_valiation, steer_validation))
        
image_train, image_valiation, steer_train, steer_validation = LoadData()
model = buildModel(image_train)
train(model, image_train, image_valiation, steer_train, steer_validation)
