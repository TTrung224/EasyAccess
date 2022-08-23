import cv2
import os
from functions import draw_text, draw_rectangle, detect_face
import pickle
import detect_mask_video
import requests
import json
from tensorflow.keras.models import load_model
from registration import getUpperFaceImg

server_address = 'http://127.0.0.1:5000/modify_status'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dictionaryDir = os.path.join(BASE_DIR, "data/labels.pickle")
fullFaceTrainerDir = os.path.join(BASE_DIR, "data/fullFaceTrainer.yml")
upperFaceTrainerDir = os.path.join(BASE_DIR, "data/upperFaceTrainer.yml")


prototxtPath = os.path.join(BASE_DIR, "face_detector/deploy.prototxt")
weightsPath = os.path.join(
    BASE_DIR, "face_detector/res10_300x300_ssd_iter_140000.caffemodel")
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
maskNet = load_model("mask_detector.model")


# function to predict the person label
def predict(test_img, face_recogniser, subjects):
    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    try:
        # detect face from the image
        face, rect = detect_face(img, faceNet)
        # predict the image using our face recognizer
        label, percent = face_recogniser.predict(face)
        percent = round(100 - percent)
        # print(label, percent)

        if percent < 60:
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, "unknown", rect[0], rect[1] - 5)
        else:
            # get name of respective label returned by face recognizer
            percent = "{0}%".format(percent)
            label_text = subjects[str(label)][0] + " - " + percent
            dict_holder = {"status": True, "ID": str(
                label), "name": subjects[str(label)][0]}
            try:
                s = requests.post(
                    server_address, json=json.dumps(dict_holder)).content
            except Exception:
                pass
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, label_text, rect[0], rect[1] - 5)
    finally:
        return img


def upperFacePredict(test_img, face_recogniser, subjects):
    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    try:
        # detect face from the image
        face, rect = getUpperFaceImg(img)
        # predict the image using our face recognizer
        label, percent = face_recogniser.predict(face)
        percent = round(100 - percent)
        # print(label, percent)

        if percent < 40:
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, "unknown", rect[0], rect[1] - 5)
        else:
            # get name of respective label returned by face recognizer
            percent = "{0}%".format(percent)
            label_text = subjects[str(label)][0] + " - " + percent
            dict_holder = {"status": True, "ID": str(
                label), "name": subjects[str(label)][0]}
            try:
                s = requests.post(
                    server_address, json=json.dumps(dict_holder)).content
            except Exception:
                pass
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, label_text, rect[0], rect[1] - 5)
    finally:
        return img


# main function to recognise people
def recognise(image_hub):
    with open(dictionaryDir, 'rb') as file:
        subjects = pickle.load(file)
        file.close()

    # create our LBPH face recognizer
    face_recogniser = cv2.face.LBPHFaceRecognizer_create()
    upper_face_recogniser = cv2.face.LBPHFaceRecognizer_create()
    face_recogniser.read(fullFaceTrainerDir)
    upper_face_recogniser.read(upperFaceTrainerDir)
    # face_recogniser = functions.train(face_recogniser)
    # cap = cv2.VideoCapture(1)

    while True:
        # ret, img = cap.read()
        try:
            rpi_name, img = image_hub.recv_image()
            image_hub.send_reply(b'OK')
            if img is None:
                continue
        except Exception:
            continue

        detect_result = detect_mask_video.mask_detector(img, faceNet, maskNet)
        print(detect_result)
        if detect_result is True:
            img = upperFacePredict(img, upper_face_recogniser, subjects)
            ret, jpg = cv2.imencode('.jpg', img)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() +
                   b'\r\n\r\n')
        else:
            img = predict(img, face_recogniser, subjects)
            ret, jpg = cv2.imencode('.jpg', img)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() +
                   b'\r\n\r\n')