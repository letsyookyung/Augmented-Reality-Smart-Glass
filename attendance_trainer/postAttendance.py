import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3
from datetime import date,datetime
from post_date_time import post_date_time

def getprofileId(ID):
    conn=sqlite3.connect('FaceBase.db')
    cmd='SELECT * FROM people WHERE ID=%s'%(str(ID))
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

def postatt(ID,prd):
    conn=sqlite3.connect('attendanceBase.db')
    conn.execute('UPDATE attendance SET '+str(prd)+'=?'+'WHERE ID =?',('Present',ID))
    conn.commit()
    conn.close()


faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(1);
path='Datasets'

rec = cv2.face.LBPHFaceRecognizer_create()
rec.read('trainer/trainer.yml')

ID=0
font=cv2.FONT_HERSHEY_SIMPLEX
prd=input("\nEnter the period(p) with number to post attendance .\nEx : p1\n")
while True:
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(100,100),flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        ID,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getprofileId(ID)
        postatt(ID,prd)
        post_date_time(ID,prd)
        if profile != None:
            cv2.putText(img,'Hiii '+str(profile[2]),(x,y+h+30),cv2.FONT_HERSHEY_TRIPLEX,1,(255,144,30),2)
            cv2.putText(img,'Your Attendance is Posted ',(x,y+h+60),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(30,144,255),2)
            #cv2.putText(img,'At Date & Time :',d_t[0],(x,y+h+60),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,69255),2)
    cv2.imshow('Face',img)
    if cv2.waitKey(20)==ord('q') :
        break
cam.release()
cv2.destroyAllWindows()
