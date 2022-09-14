from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import cv2
import os
import numpy as np
from datetime import date, datetime


# function to draw a rectangle around an object
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


# function to add text to a rectangle
def draw_text(img, text, x, y):
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 2.5, 3)
    cv2.rectangle(img, (x, y), (x + w, y - (h+5)), (90, 90, 90), -1)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN,
                2.5, (25, 225, 25), 3)




def detect_face(net, frame, conf_threshold=0.7):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [
        104, 177, 123], False, False,)

    net.setInput(blob)
    detections = net.forward()
    box = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)

            x = x1
            y = y1
            w = x2 - x1
            h = y2 - y1

            box.append([x, y, w, h])
            #  blurry rectangle to the detected face
            # face = gray[right:right+left, top:top+bottom]
            # gray[right:right+face.shape[0], top:top+face.shape[1]] = face
        if len(box) == 0:
            return None, None

        return gray[y:y + h, x:x + w], tuple(box[0])
