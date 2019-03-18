import cv2
import time
from datetime import datetime

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")

motion_list = []
img_counter = 0
firstFrame = None

while True:
    ret, frame = cam.read()
    height, width, layers = frame.shape
    h = int(height/2)
    w = int(width/2)
    resize = cv2.resize(frame, (w, h))

    cv2.imshow("test", resize)

    if not ret:
        break
    
    k = cv2.waitKey(1)
    
    if k%256 == 27:
        print("Escape hit")
        break

    elif k%256 == 109:
        while True:
            # m key = motion
            motion = 0
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if firstFrame is None:
                firstFrame = gray
                continue

            diff_frame = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations = 2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in cnts:
                if cv2.contourArea(contour) < 1000:
                    print("A")
                    continue
                motion = 1
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            motion_list.append((motion, datetime.now()))

            height, width = gray.shape
            h = int(height/2)
            w = int(width/2)
            resize2 = cv2.resize(gray, (w, h))
            cv2.imshow("Gray", resize2)
        
            ka = cv2.waitKey(1)
            if ka%256 == 27:
                break


