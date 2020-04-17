import speech_recognition as sr
import subprocess
import cv2
import numpy as np
import pyaudio
from PIL import Image
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

names = ['박서윤','이유경','김준표','김하은','현광수','차의성','하상집']

r = sr.Recognizer()
mic = sr.Microphone()

def microphone(r,mic):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    raw = r.recognize_google(audio,language='ko-KR')
    return raw

def name_similar(m, name_list):
    stu_name=[]
    max = 0.35
    for i,j in enumerate(name_list):
        if similar(m,j) > max:
            stu_id = i+1
            stu_name.append(j)
            max = similar(m,j)
    if stu_name:
        print("정상입력되었습니다.")
        return stu_id
    else:
        print("다시 말씀해주시겠어요?")
        m = microphone(r,mic)
        stu_id1 = name_similar(m, name_list)
        return stu_id1
