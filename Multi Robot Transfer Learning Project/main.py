# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 02:17:40 2017

@author: peps
"""

from init import initEnv
from fc_neuralnet import getCompiledModel
import sensor
import train

if __name__ == "__main__":
    clientID, start_pos, goal_pos = initEnv()
    image = sensor.getCurrentImage()
    #get feature map from CNN
    #featureMap = getFeatureMap()
    initialState = [-1, -1, -1]
    
    model = getCompiledModel()
    train.training(model)