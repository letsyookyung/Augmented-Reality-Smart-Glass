import cv2, pickle, os
import numpy as np
from collections import deque
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

with open("range.pickle", "rb") as f:
	t = pickle.load(f)

hsv_lower = np.array([t[0], t[1], t[2]])
hsv_upper = np.array([t[3], t[4], t[5]])

cap = cv2.VideoCapture(0)
points = []
loca = []

p_img = cv2.imread('slides_0.png', cv2.IMREAD_COLOR)
#cv2.namedWindow('PPTX',cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty('PPTX',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
a = list()
b=list()
p_img = cv2.resize(p_img, dsize=(600, 480), interpolation=cv2.INTER_AREA)
flag = 0
slide_num = 0
buff = 500
line_pts = deque(maxlen=buff)

while(True):

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    filterFrame = cv2.medianBlur(frame, 15)
    filterFrame = cv2.GaussianBlur(frame, (35, 35), 25)

    hsvFrame = cv2.cvtColor(filterFrame, cv2.COLOR_BGR2HSV)

    lower_bound = hsv_lower
    upper_bound = hsv_upper

    threshImg = cv2.inRange(hsvFrame, lower_bound, upper_bound)
    blur = cv2.medianBlur(threshImg, 15)
    blur = cv2.GaussianBlur(blur, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img_cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    contours,_ = cv2.findContours(threshImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    finalImg = cv2.bitwise_and(frame, frame, mask=threshImg)
    finalImg = cv2.drawContours(finalImg, contours, -1, (255, 0, 0), 1)


    X_ = 0
    Y_ = 0
    c_ = 0

    key = cv2.waitKey(1)

    if flag == 1:
        p_img = cv2.imread('slides_' + str(slide_num) + '.png', cv2.IMREAD_COLOR)
        p_img = cv2.resize(p_img, dsize=(600, 480), interpolation=cv2.INTER_AREA)
        if len(img_cnts) >= 1:
            b=[]
            cnt = max(img_cnts, key=cv2.contourArea)
            if cv2.contourArea(cnt) > 250:
                M = cv2.moments(cnt)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                line_pts.appendleft(center)
                for i in range(1, len(line_pts)):
                    if line_pts[i - 1] is None or line_pts[i] is None:
                        continue
                    cv2.line(p_img , line_pts[i - 1], line_pts[i], (0, 0, 255), 3)
        elif len(img_cnts) == 0:
            b.append(1)
            if len(line_pts) != []:
                p_img_gray = cv2.cvtColor(p_img , cv2.COLOR_BGR2GRAY)
                filterFrame1 = cv2.medianBlur(p_img_gray, 15)
                filterFrame1 = cv2.GaussianBlur(filterFrame1, (5, 5), 0)
                thresh1 = cv2.threshold(filterFrame1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                p_img_cnts = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
                if len(p_img_cnts) >= 1:
                    cnt = max(p_img_cnts, key=cv2.contourArea)
            print(len(b))
            if len(b) > 12 and len(b)<24:
                flag = 0
                b=[]
            else:
                line_pts = deque(maxlen=500)
                p_img = cv2.imread('slides_' + str(slide_num) + '.png', cv2.IMREAD_COLOR)
                p_img = cv2.resize(p_img, dsize=(600, 480), interpolation=cv2.INTER_AREA)


    #
    if flag==0:

        for item in contours:
            for i in item:
                X_ += i[0][0]
                Y_ += i[0][1]
                c_ += 1
        try:
            if len(loca) < 2:
                loca.append([int(X_ / c_), int(Y_ / c_)])
                cv2.circle(p_img, tuple(loca[0]), 5, (0, 255,0), -1)
            else:
                key=ord('r')
                loca.append([int(X_ / c_), int(Y_ / c_)])
                cv2.circle(p_img, tuple(loca[0]), 5, (0, 255,0), -1)

        except:
            delay=1
            a.append(delay)
            print(len(a))
            if (len(a)>12) and (len(a)<24):
                flag=1
                a=[]
            else:
                pass

    if (key & 0xFF == ord('s')) and flag == 0:
        flag = 1

    elif key & 0xFF == ord('s') and flag == 1:
        flag = 0

    if (key & 0xFF == ord('n')):
        points = []
        slide_num +=1
        if slide_num > 3:
            slide_num = 3
        p_img = cv2.imread('slides_'+str(slide_num)+'.png', cv2.IMREAD_COLOR)
        p_img = cv2.resize(p_img, dsize=(600, 480), interpolation=cv2.INTER_AREA)

    if (key & 0xFF == ord('b')):
        points = []
        slide_num -= 1
        if slide_num < 0:
            slide_num = 0
        p_img = cv2.imread('slides_'+str(slide_num)+'.png', cv2.IMREAD_COLOR)
        p_img = cv2.resize(p_img, dsize=(600, 480), interpolation=cv2.INTER_AREA)

    #
    if (key & 0xFF == ord('r')):
        a = []
        loca=[]
        line_pts = deque(maxlen=500)
        p_img = cv2.imread('slides_'+str(slide_num)+'.png', cv2.IMREAD_COLOR)
        p_img = cv2.resize(p_img, dsize=(600, 480), interpolation=cv2.INTER_AREA)

    if key & 0xFF == ord('q'):
        break


    cv2.imshow('cam_view', frame)
    cv2.imshow('user_view', p_img)

    # cv2.imshow('HSV', finalImg)
    # cv2.imshow('PPTX', p_img)


cv2.destroyAllWindows()
cap.release()
