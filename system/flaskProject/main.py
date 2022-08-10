import cv2
import numpy as np
import os
import functions
import pickle
import imagezmq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dictionaryDir = os.path.join(BASE_DIR, "labels.pickle")

# def recognise():
#     with open(dictionaryDir, 'rb') as file:
#         subjects = pickle.load(file)
#         file.close()
#
#     # create our LBPH face recognizer
#     face_recogniser = cv2.face.LBPHFaceRecognizer_create()
#
#     face_recogniser.read("trainer.yml")
#     # face_recogniser = functions.train(face_recogniser)
#     cap = cv2.VideoCapture(1)
#
#     try:
#         while True:
#             ret, img = cap.read()
#             img = functions.predict(img, face_recogniser, subjects)
#             cv2.imshow('webcam', img)
#             cv2.waitKey(1)
#     except:
#         cap.release()
#         cv2.destroyAllWindows()

# def recognise(img):
#     with open(dictionaryDir, 'rb') as file:
#         subjects = pickle.load(file)
#         file.close()
#
#     # create our LBPH face recognizer
#     face_recogniser = cv2.face.LBPHFaceRecognizer_create()
#
#     face_recogniser.read("trainer.yml")
#     # face_recogniser = functions.train(face_recogniser)
#     cap = cv2.VideoCapture(1)
#
#     try:
#         img = functions.predict(img, face_recogniser, subjects)
#         return img
#         # cv2.imshow('webcam', img)
#         # cv2.waitKey(1)
#     except:
#         cap.release()
#         cv2.destroyAllWindows()

def recognise(image_hub):
    with open(dictionaryDir, 'rb') as file:
        subjects = pickle.load(file)
        file.close()

    # create our LBPH face recognizer
    face_recogniser = cv2.face.LBPHFaceRecognizer_create()

    face_recogniser.read("trainer.yml")
    # face_recogniser = functions.train(face_recogniser)
    # cap = cv2.VideoCapture(1)

    while True:
        # ret, img = cap.read()
        rpi_name, img = image_hub.recv_image()
        image_hub.send_reply(b'OK')
        img = functions.predict(img, face_recogniser, subjects)
        ret, jpg = cv2.imencode('.jpg', img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() +
               b'\r\n\r\n')