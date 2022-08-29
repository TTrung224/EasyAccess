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


# function to detect existence of people face
def detect_face(img):
    # convert the test image to gray scale as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)

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


# def detect_face(frame, faceNet):
#     # grab the dimensions of the frame and then construct a blob
#     # from it
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     (h, w) = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
#                                  (104.0, 177.0, 123.0))
#
#     # pass the blob through the network and obtain the face detections
#     faceNet.setInput(blob)
#     detections = faceNet.forward()
#     print(detections.shape)
#     if (len(detections.shape) == 0):
#         return None, None
#     (x, y, w, h) = detections.shape[0]
#
#     # initialize our list of faces, their corresponding locations,
#     # and the list of predictions from our face mask network
#
#     # loop over the detections
#     # for i in range(0, detections.shape[2]):
#     #     # extract the confidence (i.e., probability) associated with
#     #     # the detection
#     #     confidence = detections[0, 0, i, 2]
#
#     #     # filter out weak detections by ensuring the confidence is
#     #     # greater than the minimum confidence
#     #     if confidence > 0.5:
#     #         # compute the (x, y)-coordinates of the bounding box for
#     #         # the object
#     #         box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#     #         (startX, startY, endX, endY) = box.astype("int")
#
#     #         # ensure the bounding boxes fall within the dimensions of
#     #         # the frame
#     #         (startX, startY) = (max(0, startX), max(0, startY))
#     #         (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
#
#     #         # extract the face ROI, convert it from BGR to RGB channel
#     #         # ordering, resize it to 224x224, and preprocess it
#     #         face = frame[startY:endY, startX:endX]
#     #         face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#     #         # face = cv2.resize(face, (224, 224))
#     #         # face = img_to_array(face)
#     #         # face = preprocess_input(face)
#
#     #         # add the face and bounding boxes to their respective
#     #         # lists
#     #         # faces.append(face)
#     #         # locs.append((startX, startY, endX, endY))
#
#     # # return a 2-tuple of the face locations and their corresponding
#     # # locations
#     return gray[y:y + w, x:x + h], detections.shape[0]

# def detect_face(net, frame, conf_threshold=0.7):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     frameHeight = frame.shape[0]
#     frameWidth = frame.shape[1]
#     blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [
#         104, 177, 123], False, False,)

#     net.setInput(blob)
#     detections = net.forward()
#     box = []
#     for i in range(detections.shape[2]):
#         confidence = detections[0, 0, i, 2]
#         if confidence > conf_threshold:
#             x1 = int(detections[0, 0, i, 3] * frameWidth)
#             y1 = int(detections[0, 0, i, 4] * frameHeight)
#             x2 = int(detections[0, 0, i, 5] * frameWidth)
#             y2 = int(detections[0, 0, i, 6] * frameHeight)
#             box.append([x1, y1, x2, y2])
#             top = x1
#             right = y1
#             bottom = x2-x1
#             left = y2-y1

#             #  blurry rectangle to the detected face
#             #  face = frame[right:right+left, top:top+bottom]
#             #  frame[right:right+face.shape[0], top:top+face.shape[1]] = face

#     return gray[x1:x2, y1:y2], tuple(box[0])
