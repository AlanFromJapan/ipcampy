# Big thanks to the below link which had all the core code needed
# https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv#49979186


import cv2
import numpy as np
import config
from flask import Flask, request, send_file, render_template, abort

from io import BytesIO

############################ FLASK VARS #################################
app = Flask(__name__, static_url_path='')

cap = None

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ico'])


############################ FLASK INIT #################################
#Will be called once at startup BEFORE loading any pages thanks to below CustomServer class
#use to init the cv2 context that takes 1-2 sec otherwise
@app.before_first_request
def init():
    global cap

    if not cap is None:
        print("DBG: recycling")
        cap.release()

    camurl = "rtsp://" + config.myconfig["login"] + ":" + config.myconfig["password"] + "@" + config.myconfig["ip"] + ":" + config.myconfig["port"]+ config.myconfig["suffix"]
    #print ("DBG: camurl = " + camurl)

    #takes 1-2 sec so do as rarely as you can
    cap = cv2.VideoCapture(camurl)



############################ Web requests ###############################

@app.route('/')
def homepage():
    return render_template("template01.html", pagename="Home")

    
@app.route('/capture.jpg')
def captureImage():
    global cap

    #read one frame (numpy.ndarray object)
    ret, frame = cap.read()

    #sometimes the capture fails and it means you're good to recycle your OpenCV capture.
    #accept to lose this frame (avoid infinite loop) and attempt recycling
    if frame is None or frame.size == 0:
        print ("DBG: empty frame, attempt recycling")
        init()
        abort(500)

    #write frame to memory buffer as JPEG
    is_success, buffer = cv2.imencode(".jpg", frame)
    io_buf = BytesIO(buffer)
    
    #put back at start in case
    io_buf.seek(0)

    #return the in memory image
    return send_file(io_buf, mimetype='image/jpeg')


########################################################################################
## Main entry point
#
if __name__ == '__main__':
    try:
        #start web interface
        app.debug = True
        # Remeber to add the command to your Manager instance
        app.run(host='0.0.0.0', port=56789, threaded=True)

    finally:
        if cap != None:
            print("Release OpenCV ...")
            cap.release()