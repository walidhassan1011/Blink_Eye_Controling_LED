import cv2 as cv 
import numpy as np
import cvzone as cvz
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.SerialModule import SerialObject
from time import sleep
from cvzone.PlotModule import LivePlot

# blink eye detection 

cap=cv.VideoCapture('Video.mp4')
arduino=SerialObject()
detector=FaceMeshDetector(maxFaces=1)

plotY=LivePlot(640,360,[20,50],invert=True)
idList=[22,23,24,26,110,157,158,159,160,161,130,243]
ratioList=[]
blinkCounter=0
counter=0
while True :

    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    success, img=cap.read()
    img, faces=detector.findFaceMesh(img,draw=False)

    if faces:
        faces=faces[0]
        for id in idList:
            cv.circle(img,faces[id],5,(255,0,255),cv.FILLED)
        leftUp=faces[159]
        leftDown=faces[23]
        leftleft=faces[130]
        leftRight=faces[243]
        lenghtVer,_=detector.findDistance(leftUp,leftDown)
        lenghtHor,_=detector.findDistance(leftleft,leftRight)
        cv.line(img,leftUp,leftDown,(0,200,0),3)
        cv.line(img,leftleft,leftRight,(0,200,0),3)
        ratio=int((lenghtVer/lenghtHor)*100)
        ratioList.append(ratio)
        if len(ratioList)>3:
            ratioList.pop(0)
        ratioAvg=sum(ratioList)/len(ratioList)

        if ratioAvg<35 and counter==0:
            arduino.sendData([1])
            blinkCounter+=1
            counter=1
        
        if counter!=0:
            arduino.sendData([0])  
            counter+=1
            if counter>10:
                counter=0
             
            color=(0,200,0)
        else:
           
            color=(255,0,255)
        
        cvz.putTextRect(img,f'Blink Count: {blinkCounter}',(50,100),colorR=color)

        print(ratio)
        imgPlot=plotY.update(ratioAvg,(0,200,0))
        img=cv.resize(img,(640,360))
        imgStack=cvz.stackImages([img,imgPlot], 2, 1)
    else:
        img=cv.resize(img,(640,360))
        imgStack=cvz.stackImages([img,img], 2, 1)


   
    cv.imshow("Video",imgStack)
    cv.waitKey(25)


# load the face cascade



