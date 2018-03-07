# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 23:04:53 2017

@author: AdityaPMishra
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 18:36:12 2017

@author: AdityaPMishra
"""

# Simple CNN model for CIFAR-10
import numpy
import random
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')
from matplotlib import pyplot
from scipy.misc import toimage
import scipy.stats as st
import matplotlib.image as mp
import argparse
from keras.callbacks import ModelCheckpoint
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers import Lambda,Activation, Flatten, Dense, Dropout
from keras.layers.normalization import BatchNormalization

def generate_batches(X,Yarray, batch_size, istraining):
    #print("yarray")
    #print(Yarray)
    images = numpy.empty([batch_size, 3,128, 128])
    while True:
        i = 0
        TorqueDiff = []
        for index in numpy.random.permutation(X.shape[0]):            
            if istraining:
                image =  mp.imread(r"G:\VRepPython\finale\imageslooper1_"+str(X[index])+".jpeg")
                image = image.astype('float32')
                image = image/255.0
                TorqueDiff1 = Yarray[X[index]]
                TorqueDiff.append(TorqueDiff1)
            else:
                image = mp.imread(r"G:\VRepPython\finale\imageslooper1_"+str(X[index])+".jpeg")
                image = image.astype('float32')
                image = image/255.0
                TorqueDiff1 = Yarray[X[index]]
                TorqueDiff.append(TorqueDiff1)
            images[i]= numpy.transpose(image)
            i += 1
            if i == batch_size:
                #print(TorqueDiff)
                #print(len(TorqueDiff))
                #print(len(images))
                break
        yield images, numpy.array(TorqueDiff)

def trainModel(args,X,y):
# fix random seed for reproducibility
    seed = 7
    numpy.random.seed(seed)
    
    # normalize inputs from 0-255 to 0.0-1.0
    #X = numpy.arange(10968)
    print(y)
    random.shuffle(X)
    ranarray = numpy.split(X,3)
    X_train = numpy.append(ranarray[0],ranarray[1])
    X_test = numpy.array(ranarray[2])
    
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(3,128,128), activation='relu', padding='same'))
    model.add(Dropout(0.5))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(Dropout(0.5))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(Dropout(0.5))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(1024, activation='relu', kernel_constraint=maxnorm(3)))
    model.add(Dropout(0.5))
    model.add(Dense(512, activation='relu', kernel_constraint=maxnorm(3)))
    model.add(Dropout(0.5))
    model.add(Dense(256, activation='relu', kernel_constraint=maxnorm(3)))
    model.add(Dropout(0.5))
    model.add(Dense(5, activation='softmax'))
    print(model.summary())

    # Compile model
    #epochs = 25
    #lrate = 0.01
    #decay = lrate/epochs
   #sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    
    numpy.random.seed(seed)
    checkpoint = ModelCheckpoint('model-{epoch:03d}.h5',
                                 monitor='val_loss',
                                 verbose=0,
                                 mode='auto')
    model.fit_generator(generate_batches(X_train,y, args.batch_size, True),
                            args.samples_per_epoch,
                            args.nb_epoch,
                            max_q_size=1,
                            validation_data=generate_batches(X_test, y, args.batch_size, False),
                            nb_val_samples=500,
                            callbacks=[checkpoint],
                            verbose=1)
    model.save_weights('my_model_weights.h5')

    # Final evaluation of the model
    #scores = model.evaluate(X_test, y_test, verbose=0)
    #print("Accuracy: %.2f%%" % (scores[1]*100))
    
    #y_train = np_utils.to_categorical(y_train)
    #print(y_train)
    #y_test = np_utils.to_categorical(y_test)
    #print(y_test)
    
    
    
    
def s2b(s):
    s = s.lower()
    return s == 'true' or s == 'yes' or s == 'y' or s == '1'

def main():
    parser = argparse.ArgumentParser(description='Multi Robot Knowledge Transfer')
    parser.add_argument('-d', help='data directory',        dest='data_dir',          type=str,   default='data')
    parser.add_argument('-t', help='test size fraction',    dest='test_size',         type=float, default=0.2)
    parser.add_argument('-k', help='drop out probability',  dest='keep_prob',         type=float, default=0.5)
    parser.add_argument('-n', help='number of epochs',      dest='nb_epoch',          type=int,   default=7)
    parser.add_argument('-s', help='samples per epoch',     dest='samples_per_epoch', type=int,   default=1000)
    parser.add_argument('-b', help='batch size',            dest='batch_size',        type=int,   default=40)
    parser.add_argument('-o', help='save best models only', dest='save_best_only',    type=s2b,   default='true')
    parser.add_argument('-l', help='learning rate',         dest='learning_rate',     type=float, default=1.0e-4)
    args = parser.parse_args()
    dFile1 = numpy.loadtxt(fname="leftVelocitylooper1.txt",dtype=numpy.float,delimiter=',')
    dFile1 = numpy.append(dFile1,numpy.loadtxt(fname="leftVelocitylooper2.txt",dtype=numpy.float,delimiter=','))
    dFile1 = numpy.append(dFile1,numpy.loadtxt(fname="leftVelocitylooper3.txt",dtype=numpy.float,delimiter=','))
    dFile1 = numpy.append(dFile1,numpy.loadtxt(fname="leftVelocitylooper4.txt",dtype=numpy.float,delimiter=','))   
    dFile2 = numpy.loadtxt(fname="rightVelocitylooper1.txt",dtype=numpy.float,delimiter=',')
    dFile2 = numpy.append(dFile2,numpy.loadtxt(fname="rightVelocitylooper2.txt",dtype=numpy.float,delimiter=','))
    dFile2 = numpy.append(dFile2,numpy.loadtxt(fname="rightVelocitylooper3.txt",dtype=numpy.float,delimiter=','))
    dFile2 = numpy.append(dFile2,numpy.loadtxt(fname="rightVelocitylooper4.txt",dtype=numpy.float,delimiter=','))
    Finaldata = dFile2 - dFile1;
    print(len(Finaldata))
    y_test=[]
    a=0;
    b=0
    c=0
    d=0
    e=0
    x=[]
    for i in range(len(Finaldata)):
        if(Finaldata[i]<-1):
            y_test.append(0)
            a=a+1
            if(a<1000):
                x.append(i) 
                print("a:"+str(i))
        if(Finaldata[i]<-0.25 and Finaldata[i]>=-1):
            y_test.append(1)
            b=b+1
            if(b<1000):
                x.append(i)
                print("b:"+str(i))
        if(Finaldata[i]<0 and Finaldata[i]>=-0.25):
            y_test.append(2)
            c=c+1
            if(c<1001):
                x.append(i)
        if(Finaldata[i]<0.25 and Finaldata[i]>=0):
            y_test.append(2)
            c=c+1
            if(c<1001):
                x.append(i)
        if(Finaldata[i]>=0.25 and Finaldata[i]<1):
            y_test.append(3)
            d=d+1
            if(d<1000):
                x.append(i)
                print("d:"+str(i))
        if(Finaldata[i]>=1):
            y_test.append(4)
            e=e+1
            if(e<1000):
                x.append(i)
                print("d:"+str(i))
    

    #print(Finaldata[10774])
    print(len(x))
    #print()
    #print(dFile2)
    #print(len(dFile1))
    #print(len(dFile2))
    trainModel(args,numpy.array(x),np_utils.to_categorical(y_test, 5))
    #trainModel(args,numpy.array(x),y_test)





if __name__ == '__main__':
    main()