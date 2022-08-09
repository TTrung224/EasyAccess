import cv2
import numpy as np
import os
import functions
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dictionaryDir = os.path.join(BASE_DIR, "labels.pickle")


with open(dictionaryDir, 'rb') as file:
    subjects = pickle.load(file)
    file.close()

# create our LBPH face recognizer
face_recogniser = cv2.face.LBPHFaceRecognizer_create()

face_recogniser.read("trainer.yml")
# face_recogniser = functions.train(face_recogniser)
cap = cv2.VideoCapture(1)

try:
    while True:
        ret, img = cap.read()
        img = functions.predict(img, face_recogniser, subjects)
        cv2.imshow('webcam', img)
        cv2.waitKey(1)
except:
    cap.release()
    cv2.destroyAllWindows()
