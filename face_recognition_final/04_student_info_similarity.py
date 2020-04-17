import speech_recognition as sr
import subprocess
import pyaudio
import cv2
import os
import numpy as np
from PIL import Image
import pickle
import load_j
import speech_similarity

id = 0
h = 70
font=cv2.FONT_HERSHEY_SIMPLEX
names = ['박서윤','이유경','김준표','김하은','현광수','차의성','하상집']

cam=cv2.VideoCapture(0);

r = sr.Recognizer()
m = sr.Microphone()


while True:
    ret, img = cam.read()
    
    img = np.full((480, 640, 3), 255, np.uint8)    
    cv2.putText(img,"Student_No", (40,70), font, 1, (255,0,0), 2)
    cv2.putText(img,"Name", (340,70), font, 1, (255,0,0), 2)
    
    for i in range(7):
        id += 1
        h += 40
        StuID, name, major, grade, attend = load_j.get_profile(str(id))
        cv2.putText(img,StuID,(40,h),font,1,(255,0,0),2)
        cv2.putText(img,name,(290,h),font,1,(255,0,0),2)

   
    cv2.rectangle(img,(20,20),(620,460), (250, 0, 0), 3,cv2.LINE_AA,0)


    cv2.imshow('image', img)

    if cv2.waitKey()==ord('q') :

        raw = speech_similarity.microphone(r,m)
        idn = speech_similarity.name_similar(raw, names)
        
        break

cam.release()
cv2.destroyAllWindows()

id = idn

while True:
    ret,img=cam.read()
    img = np.full((480, 640, 3), 255, np.uint8) 
        
    StuID, name, major, grade, attend = load_j.get_profile(str(id))
        
    img2p = "Student_list/User_"+str(id)+".jpg"
    img2 = cv2.imread(img2p,1)
    down1_img2 = cv2.pyrDown(img2)
    width1, height1, channel1 = down1_img2.shape
    face = down1_img2[0:200,25:295]
    
    img[40:240, 185:455] = face
    
    if StuID != None:
        cv2.putText(img,'Name:'+name,(175,280),font,1,(0,0,255),2)
        cv2.putText(img,'Major:'+major,(175,320),font,1,(0,0,255),2)
        cv2.putText(img,'Grade:'+grade,(175,360),font,1,(0,0,255),2)
    
    cv2.rectangle(img,(150,20),(490,460), (250, 0, 0), 3,cv2.LINE_AA,0)
    cv2.imshow('image',img)
    
    if cv2.waitKey(20)==ord('q') :
        break
cam.release()
cv2.destroyAllWindows()
