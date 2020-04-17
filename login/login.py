import cv2
import pickle
import numpy as np
import pyautogui as gui
import os
import time
import re

default_encoding_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "encodings.pickle")

with open("range.pickle", "rb") as f:
	t = pickle.load(f)


def get_AR(objects, time_):

    cap = cv2.VideoCapture(0)

    replaceImg = cv2.imread(objects+".jpg")
    rows, cols, ch = replaceImg.shape
    pts1 = np.float32([[0, 0], [cols, 0], [cols, rows], [0, rows]])  # this points are necessary for the transformation
    zoomLevel = 0.35  # when zoomLevel is positive it zooms in, when its negative it zooms out
    pts1 = pts1 + np.float32([[zoomLevel * cols, zoomLevel * rows], [-zoomLevel * cols, zoomLevel * rows],
                                  [-zoomLevel * cols, -zoomLevel * rows], [zoomLevel * cols, -zoomLevel * rows]])

    processing = True  # boolean variable using for disabling the image processing
    maskThreshold = 10
    end_time = time.time() + time_
    while (True):
        # Capture frame-by-frame
        ret, img = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # This function is used to detect the corners of the chessboard, 9x6 is the number of corners to find
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

        # If found, do the processing
        if ret == True and processing:

            pts2 = np.float32([corners[0, 0], corners[8, 0], corners[len(corners) - 1, 0], corners[len(corners) - 9, 0]])
            # compute the transform matrix
            M = cv2.getPerspectiveTransform(pts1, pts2)
            rows, cols, ch = img.shape
            # make the perspective change in a image of the size of the camera input
            dst = cv2.warpPerspective(replaceImg, M, (cols, rows))

            ret, mask = cv2.threshold(cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY), maskThreshold, 1, cv2.THRESH_BINARY_INV)
            # Erode and dilate are used to delete the noise
            mask = cv2.erode(mask, (3, 3))
            mask = cv2.dilate(mask, (3, 3))
            # The two images are added using the mask
            for c in range(0, 3):
                img[:, :, c] = dst[:, :, c] * (1 - mask[:, :]) + img[:, :, c] * mask[:, :]

        cv2.imshow('img', img)

        if time.time() > end_time:
            break

        key = cv2.waitKey(1)

        if key == ord('q'):  # quit
            print('Quit')
            break
        if key == ord('p'):  # processing
            processing = not processing
            if processing:
                print('Activated image processing')
            else:
                print('Desactivated image processing')


    cap.release()
    cv2.destroyAllWindows()



def get_keys(width, height):

	max_keys_in_a_row = 11						# max number of keys in any row is 10 i.e the first row which contains 1234567890'backspace'
	key_width = int(width/max_keys_in_a_row)	# width of one key. width is divided by 10 as the max number of keys in a single row is 11.

	row0_key_width = key_width * 11			# width of zeroth or numeric row of keys
	row1_key_width = key_width * 10			# width of first row
	row2_key_width = key_width * 9			# width of second row
	row3_key_width = key_width * 7			# width of third row
	row4_key_width = key_width * 5			# width of space
	row_keys = []							# stores the keys along with its 2 corner coordinates and the center coordinate

	# for the zeroth row
	x1, y1 = 0, int((height - key_width * 5) / 2)	# 5 is due to the fact that we will have 5 rows. y1 is set such that the whole keyboard has equal margin on both top and bottom
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1					# copying x1, x2, y1 and y2
	keys = "1 2 3 4 5 6 7 8 9 0 <-"
	keys = keys.split(" ")
	for key in keys:
		if key == "<-":
			row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 25, int((y2+y1)/2) + 10)])
		else:
			row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2					# copying back from c1, c2, c3 and c4

	# for the first row
	x1, y1 = int((row0_key_width - row1_key_width) / 2) + x1, y1 + key_width
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1					# copying x1, x2, y1 and y2
	keys = "QWERTYUIOP"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2					# copying back from c1, c2, c3 and c4

	# for second row
	x1, y1 = int((row1_key_width - row2_key_width) / 2) + x1, y1 + key_width   # x1 is set such that it leaves equal margin on both left and right side
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1
	keys = "ASDFGHJKL"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	# for third row
	x1, y1 = int((row2_key_width - row3_key_width) / 2) + x1, y1 + key_width
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1
	keys = "ZXCVBNM"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	# for the space bar
	x1, y1 = int((row3_key_width - row4_key_width) / 2) + x1, y1 + key_width
	x2, y2 = 5 * key_width + x1, key_width + y1
	c1, c2 = x1, y1
	keys = " "
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	return row_keys


def do_keypress(img, center, row_keys_points):
    pressed = ''

    for row in row_keys_points:
        arr1 = list(np.int0(np.array(center) >= np.array(row[1])))
        arr2 = list(np.int0(np.array(center) <= np.array(row[2])))


        if arr1==[1,1] and arr2 == [1,1]:

            if row[0] == '<-':
                gui.press('backspace')
                pressed+= '<'
            else:
                gui.press(row[0])
                pressed+=(row[0])
            cv2.fillConvexPoly(img, np.array([np.array(row[1]), np.array([row[1][0], row[2][1]]), np.array(row[2]), np.array([row[2][0], row[1][1]])]), (255, 0, 0))

            #print("PRESSED!!!! :", pressed)
    return img, pressed


# def update_text(sen):
#     #print("start",sen)
#     global toString
#     toString = ''.join(sen)
#     for i in range(0,len(toString)):
#         if (toString[i] == '<') and (toString[i-1] != '<'):
#             #print("inLoop",toString)
#             toString = toString[:i-1] + toString[i+1:]
#             break
#     #print("break",toString)
#     if toString.count('<') > 0:
#         #print("again",sen)
#         update_text(list(toString))

#     else:
#         pass
#        # print("done",toString)
#     return toString


def vir_key(t,access_code,nameWindow="img"):

    # access_code = access_code

    cam = cv2.VideoCapture(0)

    hsv_lower = np.array([t[0], t[1], t[2]])
    hsv_upper = np.array([t[3], t[4], t[5]])
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)  # width of video captured by the webcam
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)  # height of the video captured by the webcam

    row_keys_points = get_keys(width,height)
    new_area, old_area = 0, 0
    c, c2 = 0, 0
    flag_keypress = False
    # global sen
    sen = list()
    # print("LOADING...", sen)
    # cv2.namedWindow('POSCO', cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty('POSCO', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    text_ = ''

    while(True):
        # global text_
        img = cam.read()[1]
        img = cv2.flip(img, 1)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, hsv_lower, hsv_upper)
        blur = cv2.medianBlur(mask, 15)
        blur = cv2.GaussianBlur(blur , (5,5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        # text_ = update_text(sen)
        text_ = ''.join(sen)
        text_ = re.sub('.{1}[<]', '', text_)
        message = "ACCESS CODE: "
        cv2.putText(img, message + text_, (90, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        if len(contours) > 0:
            cnt = max(contours, key = cv2.contourArea)

            if cv2.contourArea(cnt) > 350:
                rect = cv2.minAreaRect(cnt)
                center = list(rect[0])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.circle(img, tuple(np.int0(center)), 2, (0, 255, 0), 2)
                cv2.drawContours(img,[box],0,(0,0,255),2)
                #calculation of difference of area and center
                new_area = cv2.contourArea(cnt)
                new_center = np.int0(center)
                if c == 0:
                    old_area = new_area
                c += 1
                diff_area = 0
                if c > 3:
                    diff_area = new_area - old_area
                    c = 0
                if c2 == 0:
                    old_center = new_center
                c2 += 1
                diff_center = np.array([0, 0])
                if c2 > 5:
                    diff_center = new_center - old_center
                    c2 = 0

                center_threshold = 10
                area_threshold = 200
                if abs(diff_center[0]) < center_threshold or abs(diff_center[1]) < center_threshold:

                    if diff_area > area_threshold and flag_keypress == False:
                        #좌표와 입력된 키 값 동시에 return 하게 만듬
                        img, pressed = do_keypress(img, new_center, row_keys_points)
                        print("********* PRESSED KEY: ", pressed)
                        if pressed == '<':
                            sen = sen[:-1]
                        else:
                            sen.append(pressed)
                        #cv.putText(img, 'OpenCV', location, font, fontScale, yellow, thickness)
                        flag_keypress = True
                    elif diff_area < -(area_threshold) and flag_keypress == True:
                        flag_keypress = False
            else:
                flag_keypress = False
        else:
            flag_keypress = False

        # displaying the keyboard

        for key in row_keys_points:
            # RGB -> BGR

            #cv2.putText(img, sen, (100, 20), cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 255, 0), 2)
            cv2.putText(img, key[0], key[3], cv2.FONT_HERSHEY_DUPLEX, 1, (262, 173, 93))
            cv2.rectangle(img, key[1], key[2], (255, 128,0), thickness = 3)

        cv2.imshow(nameWindow,img)
        key = cv2.waitKey(1)

        # text_ = update_text(sen)
        if ''.join(sen) == access_code or key == ord('q'):
            # key = ord('\x1B')
            break

        # '\x08' = ASCII Table = backsapce (chr(), ord() function)
        if key == ord('\x08'):
            # text_ = update_text(sen)
            text_ = ''.join(sen)
            text_ = re.sub('.{1}[<]', '', text_)
            text_ = text_[:-1]
            print(text_)
            continue

        # elif key == ord('\x1B'):
        #     text_ = update_text(sen)
        #     break

        # else:
        #     continue

    cam.release()
    cv2.destroyAllWindows()
    return True



def main():

    # get_AR("firstimage", 20)
    access_ = vir_key(t,"B4","img")
    # if access_ == True:
    #     get_AR("secondimage", 300)
    # else:
    #     print("BYE")


main()