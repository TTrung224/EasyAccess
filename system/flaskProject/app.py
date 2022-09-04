from urllib import response
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import imagezmq
import json
from flask_cors import CORS, cross_origin
import socket
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get and save the server IP address into txt file
hostname = socket.gethostname()   
IPAddress = socket.gethostbyname(hostname)
ipFile = os.path.join(BASE_DIR, "ipAddress.txt")
f = open(ipFile, "w")
f.write(IPAddress)
f.close()
print(IPAddress)

import recognise
import registration

dict = {'status': False, 'ID': '', 'name': '', 'door': False, 'temp': None, 'regisStatus': False}

app = Flask(__name__)
CORS(app, support_credentials=True)

image_hub = imagezmq.ImageHub()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recogVideo')
def recogVideo():
    return Response(recognise.recognise(image_hub),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/regisVideo', methods=["GET"])
def regisVideo():
    id = request.args.get("ID")
    return Response(registration.registerFace(id, image_hub),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/regisWithMaskVideo', methods=["GET"])
# def regisWithMaskVideo():
#     id = request.args.get("ID")
#     return Response(registration.registerMaskFace(id, image_hub),
#     mimetype='multipart/x-mixed-replace; boundary=frame')


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
    dict['regisStatus'] = False
    return render_template('regisScan.html')


# @app.route('/regisScanWithMask', methods=["GET"])
# def regisScanWithMask():
#     return render_template('regisScanWithMask.html')


@app.route('/status_send', methods=['POST'])
@cross_origin(supports_credentials=True)
def status_send():
    result = dict
    return jsonify(result)


@app.route('/reset_status', methods=['POST', 'GET'])
def reset_status():
    dict['status'] = False
    dict['ID'] = ''
    dict['name'] = ''
    return "reset done"


# modify status when main program recognize faces
@app.route('/modify_status', methods=['POST'])
def modify_status():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    dict['status'] = True
    dict['ID'] = data['ID']
    dict['name'] = data['name']
    return "message received"


# modify door status 
@app.route('/modify_door_status', methods=['POST'])
def modify_door_status():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    dict['door'] = data['door']
    return "door status updated"


# modify temperature 
@app.route('/modify_temp', methods=['POST'])
def modify_temp():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    dict['temp'] = data['temp']
    return "temperature updated"


# modify regis status
@app.route('/modify_regis_status', methods=['POST'])
def modify_regis_status():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    dict['regisStatus'] = data['regisStatus']
    return "registration status updated"


# to check status sent from main program
@app.route('/server_status_check', methods=['POST'])
def server_status_check():
    return jsonify(dict)


if __name__ == "__main__":
    app.run(debug=True)
