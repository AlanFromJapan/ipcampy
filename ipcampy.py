# Big thanks to the below link which had all the core code needed
# https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv#49979186


import cv2
import numpy as np
import config
from flask import Flask, request, send_file

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

    camurl = "rtsp://" + config.myconfig["login"] + ":" + config.myconfig["password"] + "@" + config.myconfig["ip"] + ":" + config.myconfig["port"]+ config.myconfig["suffix"]
    #print ("DBG: camurl = " + camurl)
    cap = cv2.VideoCapture(camurl)



############################ Web requests ###############################

@app.route('/')
def homepage():
    return '''Hello monde! <br/>
    <a href="capture.jpg">See the capture</a>'''

    
@app.route('/capture.jpg')
def captureImage():
    global cap

    #read one frame
    ret, frame = cap.read()

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
            cap.release()