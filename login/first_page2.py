import cv2
import time
import pickle
from face_attendance import process_attendance,attendance

from student_info import process_studentinfo, student_info
from ppt import process_ppt, ppt
from show_login import get_AR, access_keyboard, select_keyboard
from capture import VideoCaptureThreading


end = False

####
skip_access = True
skip_selection_mode = True
thread_mode = True
mode = '4'
mode1_time = 200
mode2_time = 200
mode3_time = 200
mode4_time = 200
####

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# with open("range.pickle", "rb") as f:
#     t = pickle.load(f)

tt = 5
capture = cv2.VideoCapture(0)
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)


if thread_mode:
    capture.release()
    capture = VideoCaptureThreading(0)
    capture.start()

cv2.namedWindow('Post-Glass', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Post-Glass', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

if not skip_access:
    # 로딩 화면 부분
    end = get_AR(capture, 'firstimage', tt)

    # # 최초 액세스 코드 입력 부분

    # end = access_keyboard(capture, 'B4', width, height)

while not end:
    ret, frame = capture.read()
        
    if not skip_selection_mode:
        get_AR(capture, 'secondimage', tt)
        end, mode = select_keyboard(capture, width, height)

        tt = 5
    while not end and mode != -1:
        # print('inner while')
        ret, frame = capture.read()

        if mode in [ord('1'), ord('2'), ord('3'), '1', '2', '3', '4', 27]:
            control = mode
        
        if control == ord('1') or control == '1':
            print('IN 1')
            end = process_attendance(capture, recognizer, faceCascade, mode1_time)

        elif control == ord('2') or control == '2':
            print('IN 2')
            end = student_info(capture, mode2_time)

        elif control == ord('3') or control == '3':
            print('IN 3')
            end = ppt(capture, mode3_time)

        elif control == ord('4') or control == '4':
            print('IN 4')
            end = attendance(capture, mode4_time)

        elif control == 27:
            break
        
        mode = cv2.waitKey(1)
        if mode == ord('q'):
            end = True
            break
        
        print(end, mode)
        cv2.imshow("Post-Glass", frame)
        mode = -1

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    cv2.imshow("Post-Glass", frame)

if thread_mode:
    capture.stop()
else:
    capture.release()
cv2.destroyAllWindows()