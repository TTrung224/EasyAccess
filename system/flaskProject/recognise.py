import cv2
import numpy as np
import os
from functions import draw_text, draw_rectangle, detect_face
import pickle
import imagezmq
from registration import detect_face
import detect_mask_video


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dictionaryDir = os.path.join(BASE_DIR, "data/labels.pickle")
fullFaceTrainerDir = os.path.join(BASE_DIR, "data/fullFaceTrainer.yml")
upperfaceTrainerDir = os.path.join(BASE_DIR, "data/upperFaceTrainer.yml")


# function to predict the person label
def predict(test_img, face_recogniser, subjects):
    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    try:
        # detect face from the image
        face, rect = detect_face(img)
        # predict the image using our face recognizer
        label, percent = face_recogniser.predict(face)
        percent = round(100 - percent)
        # print(label, percent)

        if percent < 50:
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, "unknown", rect[0], rect[1] - 5)
        else:
            # get name of respective label returned by face recognizer
            percent = "{0}%".format(percent)
            label_text = subjects[str(label)][0] + " - " + percent

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
    face_recogniser2 = cv2.face.LBPHFaceRecognizer_create()
    face_recogniser.read(fullFaceTrainerDir)
    face_recogniser2.read(upperFaceTrainerDir)
    # face_recogniser = functions.train(face_recogniser)
    # cap = cv2.VideoCapture(1)

    while True:
        # ret, img = cap.read()
        rpi_name, img = image_hub.recv_image()
        image_hub.send_reply(b'OK')
        detect_result = detect_mask_video.mask_detector(img)
        if detect_result == True:
            img = predict(img, face_recogniser2, subjects)
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
