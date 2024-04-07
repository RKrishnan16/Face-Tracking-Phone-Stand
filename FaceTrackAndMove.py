

import cv2
from picamera2 import Picamera2
import time
import numpy as np

picam2 = Picamera2()

from servo import Servo
from time import sleep


pan = Servo(pin=17) # pan_servo_pin (BCM)
tilt = Servo(pin=27) 
freq = 50 # 50 Hz pwm
error = 40
errorMax = 90
# Set initial Motor position
panAngle =10
tiltAngle =-50
pan.set_angle(10)
tilt.set_angle(-50)

dispW=480
dispH=600
picam2.preview_configuration.main.size = (dispW,dispH)
picam2.preview_configuration.main.format = "RGB888"
#picam2.preview_configuration.controls.FrameRate=15
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
fps=0
pos=(15,30)
font=cv2.FONT_HERSHEY_SIMPLEX
height=0.5
weight=2
myColor=(255,255,255)

faceCascade=cv2.CascadeClassifier('/home/rohanpi/Documents/Face_Tracking_Phone_Stand/haar/haarcascade_frontalface_default.xml')
Xdir = 0
Ydir = 0
sentryStepSizeX = 2
sentryStepSizeY = 10
sentryElapsed=0
sentryTimerStart=time.time()

def SlowMoveTilt(startPos,endPos):
    dist = endPos-startPos
    absdist = int(abs(dist))
    for x in range(0,absdist):
        sleep(.05)
        if dist > 0:
            tilt.set_angle(startPos+1)
            startPos = startPos+1
        if dist < 0:
            tilt.set_angle(startPos-1)
            startPos = startPos-1
    return(startPos)
    

print("Running!")
while True:
    tStart=time.time()
    frame= picam2.capture_array()
    #frame=cv2.flip(frame,-1)
    #frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Turn frame grayscale
    faces=faceCascade.detectMultiScale(frame,1.3,5,0,(50,50)) # (window,scaleFactor,minNeighbors,Flags,(minSize,maxSize))
    #print(sentryElapsed)
    #cv2.putText(frame,str(int(fps))+' FPS',pos,font,height,myColor,weight)
    """
    if len(faces) != 0:
        sentryTimerStart = tStart
        
    sentryTimerEnd = time.time()
    sentryElapsed = sentryTimerEnd-sentryTimerStart
    if sentryElapsed >= 10:
        #print("sentry Mode")
        #print("Tilt Angle: "+ str(tiltAngle))
        if Xdir == 0: 
            panAngle = panAngle+sentryStepSizeX
            if panAngle>=90:
                panAngle=90
                Xdir = 1
                if Ydir == 0:
                    newtiltAngle = tiltAngle+sentryStepSizeY
                    if tiltAngle>=0:
                        tiltAngle=0
                        Ydir = 1
                    tiltAngle=SlowMoveTilt(tiltAngle,newtiltAngle)
                elif Ydir == 1:
                    newtiltAngle = tiltAngle-sentryStepSizeY
                    if tiltAngle<=-70:
                        tiltAngle=-70
                    tiltAngle=SlowMoveTilt(tiltAngle,newtiltAngle)
                    
            pan.set_angle(panAngle)
        elif Xdir==1:
            panAngle = panAngle-sentryStepSizeX
            if panAngle<=-90:
                panAngle=-90
                Xdir = 0
                if Ydir == 0:
                    newtiltAngle = tiltAngle+sentryStepSizeY
                    if tiltAngle>=0:
                        tiltAngle=0
                        Ydir = 1
                    tiltAngle=SlowMoveTilt(tiltAngle,newtiltAngle)
                elif Ydir == 1:
                    newtiltAngle = tiltAngle-sentryStepSizeY
                    if tiltAngle<=-70:
                        tiltAngle=-70
                    tiltAngle=SlowMoveTilt(tiltAngle,newtiltAngle)
            pan.set_angle(panAngle)
"""

            
        
        
        
    for face in faces:
        x,y,w,h=face
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),3) # draws the rectangle
        Xerror=(x+w/2)-dispW/2
        Yerror=(y+h/2)-dispH/2
        
        panAngle = panAngle-Xerror/30
        if panAngle<-90:
            panAngle=-90
        if panAngle>90:
            panAngle=90
        print(str(panAngle)+' pan   '+str(tiltAngle)+' tilt   ' + str(fps) + ' fps')
        if ((abs(Xerror)>error) and (abs(Xerror) < errorMax)):
            pan.set_angle(panAngle)
        
        tiltAngle = tiltAngle-Yerror/80
        if tiltAngle<-70:
            tiltAngle=-70
        if tiltAngle>0:
            tiltAngle=0
        if ((abs(Yerror)>error) and (abs(Yerror) < errorMax)):
            tilt.set_angle(tiltAngle)
        
    
    
    #cv2.imshow('Camera',frame)
    #print(panAngle)
    if cv2.waitKey(1)==ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)
              
cv2.destroyAllWindows()


