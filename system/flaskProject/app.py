from urllib import response
from flask import Flask, render_template, Response
from camera import RecogVideo , RegisVideo, RegisWithMaskVideo

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recogVideo')
def recogVideo():
    return Response(gen(RecogVideo()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/regisVideo')
def regisVideo():
    return Response(gen(RegisVideo()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/regisWithMaskVideo')
def regisWithMaskVideo():
    return Response(gen(RegisWithMaskVideo()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/registration')
def regisPage():
    return render_template('registration.html')

@app.route('/regisScan')
def regisScan():
    return render_template('regisScan.html')

@app.route('/regisScanWithMask')
def regisScanWithMask():
    return render_template('regisScanWithMask.html')

app.run(debug=True)
