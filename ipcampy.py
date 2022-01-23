#https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv#49979186


import cv2
import numpy as np
import config
from flask import Flask, render_template, redirect, url_for, request, make_response, send_file

from io import BytesIO

############################ FLASK INIT #################################
app = Flask(__name__, static_url_path='')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ico'])

############################ Web requests ###############################

@app.route('/')
def homepage():
    return '''Hello monde! <br/>
    <a href="capture.jpg">See the capture</a>'''

    
@app.route('/capture.jpg')
def captureImage():
    camurl = "rtsp://" + config.myconfig["login"] + ":" + config.myconfig["password"] + "@" + config.myconfig["ip"] + ":" + config.myconfig["port"]+ config.myconfig["suffix"]

    cap = cv2.VideoCapture(camurl)

    ret, frame = cap.read()

    #.save(byte_io, 'PNG')
    is_success, buffer = cv2.imencode(".jpg", frame)
    io_buf = BytesIO(buffer)
    
    io_buf.seek(0)

    cap.release()

    return send_file(io_buf, mimetype='image/jpeg')


########################################################################################
## Main entry point
#
if __name__ == '__main__':
    try:
        #start web interface
        app.debug = True
        app.run(host='0.0.0.0', port=56789, threaded=True)

    finally:
        pass