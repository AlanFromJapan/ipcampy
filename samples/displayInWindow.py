#https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv#49979186
#Works fine!

import cv2
import numpy as np
import config
import sys

camurl = "rtsp://" + config.myconfig["login"] + ":" + config.myconfig["password"] + "@" + config.myconfig["ip"] + ":" + config.myconfig["port"]+ config.myconfig["suffix"]
#print("DBG: " + camurl)

cap = cv2.VideoCapture(camurl)

while(True):
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (300, 300))
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
