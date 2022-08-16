import cv2
import os
import numpy as np
from datetime import date, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
trainingDataDir = os.path.join(BASE_DIR, "fullFace_training_data")


# function to draw a rectangle around an object
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


# function to add text to a rectangle
def draw_text(img, text, x, y):
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 2.5, 3)
    cv2.rectangle(img, (x, y), (x + w, y - (h+5)), (90, 90, 90), -1)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.5, (25, 225, 25), 3)


# function to detect existence of people face
def detect_face(img):
    # convert the test image to gray scale as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # for x, y, w, h in faces:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

    # if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None

    # under the assumption that there will be only one face,
    # extract the face area
    (x, y, w, h) = faces[0]

    # return only the face part of the image
    return gray[y:y + w, x:x + h], faces[0]
