#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this script searches for perlonged intervals of movement in highspeed
slitscan cameras
"""
#parameter
#threshold to register movement orthogonal to slitscan, tune to your footag
epsilon = 252504
#suffix frames added to interval
sigma = 0
#prefix frames added to interval
phi = 0
#max distanze between frames to be considered in the same interval of movement
delta = 12

filepath = 'train_stiched0001-0863.avi'
# 0 => vertical stripers, 1 => horizontal stripes
gradient = 0
#show gradient for debugging purposes
show = False

import cv2
import numpy as np

frameList = []

cap = cv2.VideoCapture(filepath)

if not cap.isOpened():
    print ("errors opening video file")

e1 = cv2.getTickCount()
frameCounter = 0
while cap.isOpened():

    frameCounter += 1    
    ret,frame = cap.read()
    if ret:    
        #convert to BW, derive vertically, square to lose negative numbers
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        arr = np.array(frame)
        arr = np.diff(arr,axis=gradient)
        arr = np.power(arr,2)
        
        if (arr.sum() > epsilon):
            frameList.append(frameCounter)
            
        if (show):
            cv2.imshow('ABC',arr)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break
    
#print(frameList)    
print(frameCounter)
if show: print (frameList)
#clustering frames
intervals = []
first_frame = frameList[0]
last_frame = frameList[0]
current_frame = frameList[0]

while frameList:
    while frameList and (current_frame - last_frame < delta):
        last_frame = current_frame
        current_frame = frameList.pop(0)
    intervals.append( (first_frame - phi,last_frame + sigma) )
    first_frame = current_frame
    last_frame = current_frame
    
#2DOfiler short ones out
e2 = cv2.getTickCount()
print (intervals)
if show: print ( (e2-e1) / cv2.getTickFrequency() )

cap.release()
cv2.destroyAllWindows()
