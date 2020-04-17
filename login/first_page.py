import cv2
import time
import pickle
from face_attendance import process_attendance
from student_info import process_studentinfo
from ppt import process_ppt
from show_login import get_AR, access_keyboard, select_keyboard


capture = cv2.VideoCapture(0)
control = -1
name_id = None
idn = None
flag = None

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

with open("range.pickle", "rb") as f:
    t = pickle.load(f)

tt = 10
cv2.namedWindow('Post-Glass', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Post-Glass', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 로딩 화면 부분
get_AR(capture, 'firstimage', tt)

# # 최초 액세스 코드 입력 부분
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

access_keyboard(t, capture, 'B4', width, height)

while True:
    ret, frame = capture.read()
    get_AR(capture, 'secondimage', tt)
    k = select_keyboard(t, capture, width, height)

    end_time = time.time() + 4
    tt = 10
    while True:
        ret, frame = capture.read()
        # k = cv2.waitKey(3) & 0xff  # Press 'ESC' for exiting video

        if k in [ord('1'), ord('2'), ord('3'), ord('4'), '1', '2', '3', '4', 27]:
            control = k

        if control == ord('1') or control == '1':
            print('IN 2')
            process_attendance(capture, recognizer, faceCascade, tt)

        elif control == ord('2') or control == '2':
            print('IN 2')
            k = cv2.waitKey(3) & 0xff
            if k in [ord('1'), ord('2'), ord('3'), ord('4'), 27]:
                control = k

            if name_id:
                frame, control, idn = process_studentinfo(frame, control, name_id)
            elif idn:
                frame, control, idn = process_studentinfo(frame, control, idn)
            else:
                frame, control, idn = process_studentinfo(frame, control)

        elif control == ord('3') or control == '3':
            print('IN 3')
            if flag:
                frame, control, flag = process_ppt(frame, control, flag)
            else:
                frame, control, flag = process_ppt(frame, control)

        elif control == 27:
            break
        
        cv2.waitKey(1)
        cv2.imshow("Post-Glass", frame)
        
        if time.time() > end_time:
            break

    cv2.waitKey(1)
    cv2.imshow("Post-Glass", frame)

capture.release()
cv2.destroyAllWindows()