import cv2
import numpy as np
import sqlite3


def insertOrUpdate(ID,StuID,Name,Major,Grade):
    #connecting to the db
    conn=sqlite3.connect('FaceBase.db')
    
    #check if id already exists
    cmd='SELECT * FROM people WHERE ID=%s'%str(ID)
    #returning the data in rows
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if (isRecordExist==1):
        cmd="UPDATE people SET StuID="+str(StuID)+" WHERE ID="+str(ID)
    else:
        cmd='INSERT INTO people(ID,StuID,Name,Major,Grade) VALUES('+str(ID)+','+str(StuID)+','+str(Name)+','+str(Major)+','+str(Grade)+')'
    
    conn.execute(cmd)
    conn.commit()
    conn.close()

ID=input('\nEnter your ID :')
stuid=input('\nEnter your Student ID :')
name=input('\nEnter your Name :')
major=input('\nEnter your Major :')
grade=input('\nEnter your grade :')

insertOrUpdate(ID,stuid,name,major,grade)

cam=cv2.VideoCapture(0);
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');

sn=0                    # sample number
while True:
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        sn=sn+1
        cv2.imwrite('Datasets/User'+'.'+str(ID)+'.'+str(sn)+'.jpg',gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.waitKey(100)
    cv2.imshow('Face',img)
    cv2.waitKey(1)
    if sn>29 :
        break
cam.release()
cv2.destroyAllWindows()
