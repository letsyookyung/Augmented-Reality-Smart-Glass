import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3

def getprofileId(id):
    conn=sqlite3.connect('FaceBase.db')
    cmd='SELECT * FROM people WHERE ID=%s'%(str(ID))
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);
path='Datasets'
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read('trainer/trainer.yml')
ID=0
font=cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(100,100),flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        ID,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getprofileId(ID)

        if profile != None:
            cv2.putText(img,'Name:'+str(profile[2]),(x,y+h+20),font,1,(0,0,255),2)
            cv2.putText(img,'Major:'+str(profile[3]),(x,y+h+50),font,1,(0,0,255),2)
            cv2.putText(img,'Grade:'+str(profile[4]),(x,y+h+80),font,1,(0,0,255),2)
    cv2.imshow('Face',img)
    if cv2.waitKey(20)==ord('q') :
        break
cam.release()
cv2.destroyAllWindows()
