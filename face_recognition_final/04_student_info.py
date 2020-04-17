import speech_recognition as sr
import subprocess
import pyaudio
import cv2
import os
import numpy as np
from PIL import Image
import pickle
import load_j


#this is called from the back ground thread
def return_name(r, audio):
    #received audio data, now we'll recognize it using Google Speech Recognition
    try:
        outp = r.recognize_google(audio,language='ko-KR')
        
        WORDS1 = ['하상집', '화상 집', '화상집', '가상 집', '사상 집', '상집', '하상식', '하상 집', '화장실', '하상진', '화성 집', '하성식', '화성시', '화성 집', '빵집', '집', '왕 집', '방 집', '화상 집', '화상집', '가상 집', '하 상집', '사상 집', '화상 집', '사당 집', '마당 집', '상 집', '장집', '상지', '상직', '화성집', '황 집', '10', '십']
        WORDS2 = ['김준표', '김중표', '음표', '홍준표', '김종표', '김진표', '임종표', '진표', '쉼표', '증표', '김표', '준표', '임준표', '김준교', '김준 줘', '금전초', '무슨 초', '전초', '준 표', '전표', '공준표']
        WORDS3 = ['차의성', '자위성', '자 위성', '자위 성', '차 위성', '차이성', '하울의 성', '합의성', '한의성', '의성', '차에 성', '위성', '이성', '휘성', '미성', '성', '차에 의성', '차의 성', '차의 의성', '차 에 성', '차 에 위성', '차 에 이성', '차 에 유성', '차 에 음성', '창의성', '자의성 이', '차 의성', '자의 성', '차혜성', '참외 성', '차에 성', '혜성', '전송', '창의성', '차이성', '위성', '차 위성', '의성', '인성', '음성', '위성', '은성', '차 위성', '사위성', '타이 성', '바위성', '차이성', '하이성', '희성', '이성우', '의성어', '하일성', '아이성', '아이 성', '차 이성', '차이정', '사이 성']
        WORDS4 = ['현광수', '변광수', '형광 수', '형 광수', '전광수', '향수', '방수', '장수', '강수', '양수', '전광수', '장광수', '정광수', '변광수', '형광 수', '편광 수', '형 광수', '형광 수', '형 광수', '현 광수', '현광 수', '광수', '왕수', '홍광수', '김광수', '임광수', '광숙']
        WORDS5 = ['박서윤','박소윤','서윤','더윤','허윤','서현', '서연', '소윤', '소연','어윤','어 윤', '서윤이', '서윤아', '서윤희']
        WORDS6 = ['이유경','이우경','유경','이효경','이윤경','2 6 0','6 0','E60','여경','육영','구경','우경']
        WORDS7 = ['김하은','임하은','김하온','김하운','김하원','하은이','하은아','하은','가은','다은','나은','아 응']

        WORDS = [WORDS1,WORDS2,WORDS3,WORDS4,WORDS5,WORDS6,WORDS7]
        
        for i in WORDS:
            if outp in i:
                if i[0] == '하상집':
                    ID = '7'
                elif i[0] == '김준표':
                    ID = '3'           
                elif i[0] == '차의성':
                    ID = '6'
                elif i[0] == '현광수':
                    ID = '5'
                elif i[0] == '박서윤':
                    ID = '1'
                elif i[0] == '이유경':
                    ID = '2'
                elif i[0] == '김하은':
                    ID = '4'
                else:
                    pass 
        return ID
    
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

id = 0
h = 70
font=cv2.FONT_HERSHEY_SIMPLEX

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

        with m as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        idn = return_name(r, audio)
        
        break

cam.release()
cv2.destroyAllWindows()

id = idn

while True:
    ret,img=cam.read()
    img = np.full((480, 640, 3), 255, np.uint8) 
        
    StuID, name, major, grade, attend = load_j.get_profile(id)
        
    img2p = "Student_list/User_"+id+".jpg"
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
