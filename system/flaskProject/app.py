from urllib import response
from flask import Flask, render_template, Response, request, redirect, url_for
import imagezmq
import main
import registration

app = Flask(__name__)

image_hub = imagezmq.ImageHub()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recogVideo')
def recogVideo():
    return Response(main.recognise(image_hub),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/regisVideo', methods=["GET"])
def regisVideo():
    id = request.args.get("ID")
    return Response(registration.registerNormalFace(id, image_hub),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/regisWithMaskVideo', methods=["GET"])
def regisWithMaskVideo():
    id = request.args.get("ID")
    return Response(registration.registerMaskFace(id, image_hub),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/registration')
def regisPage():
    return render_template('registration.html')


@app.route('/register', methods=["GET"])
def register():
    id = request.args.get("ID")
    name = request.args.get("Name")
    type = request.args.get("type")
    expiration = request.args.get("expireDate")

    case = registration.registerGetInfo(id, name, type, expiration)
    if case == "wrong-id":
        return redirect("registration?error=wrongId")
    elif case == "existed":
        return redirect("registration?error=existed")
    elif case == "wrong-date":
        return redirect("registration?error=wrongDate")
    return redirect("regisScan?ID=" + case)


@app.route('/regisScan', methods=["GET"])
def regisScan():
    return render_template('regisScan.html')


@app.route('/regisScanWithMask', methods=["GET"])
def regisScanWithMask():
    return render_template('regisScanWithMask.html')


app.run(debug=True)
