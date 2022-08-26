import os

import cv2
import pickle
import datetime
# import numpy
#
# # using cv2.CascadeClassifier
# # See https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
# # See more Cascade Classifiers https://github.com/opencv/opencv/tree/4.x/data/haarcascades
#
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#
# def detect(img):
#
#
#     # changing the image to gray scale for better face detection
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     faces = face_cascade.detectMultiScale(
#         gray,
#         scaleFactor=2,  # Big reduction
#         minNeighbors=5  # 4-6 range
#     )
#
#     # drawing a rectangle to the image.
#     # for loop is used to access all the coordinates of the rectangle.
#     for x, y, w, h in faces:
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
#     return img
#
#
# cap = cv2.VideoCapture(1)
#
# while True:
#     ret, img = cap.read()
#     img = detect(img)
#     cv2.imshow('webcam', cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
#     cv2.waitKey(1)
#
# cap.release()
# cv2.destroyAllWindows()


"""****************"""

# subjects = {}
# subjects = {'13891724': ['Trung', datetime.datetime(2022, 8, 16, 9, 41, 26, 497436), datetime.date(2022, 8, 18)], '13852304': ['Thong', datetime.datetime(2022, 8, 16, 9, 45, 20, 128046), datetime.date(2022, 8, 18)]}
#
# with open("data/labels.pickle", 'wb') as file:
#     pickle.dump(subjects, file)
#     file.close()
#
#
# with open('data/labels.pickle', 'rb') as file:
#     subjects = pickle.load(file)
#     file.close()
#
# print(subjects)


"""****************"""
from functions import detect_face
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
faceTrainingDataDir = os.path.join(BASE_DIR, "face_training_data")
dictionaryDir = os.path.join(BASE_DIR, "data/labels.pickle")
fullFaceTrainerDir = os.path.join(BASE_DIR, "data/fullFaceTrainer.yml")
upperFaceTrainerDir = os.path.join(BASE_DIR, "data/upperFaceTrainer.yml")
upperFaceRatio = 0.5

def retrain():
    print("Retrain face data:")
    print("Preparing data...")

    dataDirs = os.listdir(faceTrainingDataDir)

    # list to hold all subject faces
    fullFaces = []

    # list to hold all subject upper faces
    upperFaces = []

    # list to hold labels for all subjects
    labels = []

    for dirName in dataDirs:

        # ignore system files like .DS_Store
        if dirName.startswith("."):
            continue

        # extract label number of subject from dir_name
        label = int(dirName)

        userDir = faceTrainingDataDir + "/" + dirName
        # get the images names that are inside the given subject directory
        subject_images_names = os.listdir(userDir)

        # go through each image name, read image,
        # detect face and add face to list of faces
        for image_name in subject_images_names:

            # ignore system files like .DS_Store
            if image_name.startswith("."):
                continue

            # build image path
            image_path = userDir + "/" + image_name

            # read image
            image = cv2.imread(image_path)

            # detect face
            face, rect = detect_face(image)

            if face is not None:
                # add label for this face
                labels.append(label)

                # add face to list of faces
                fullFaces.append(face)

                # add upper face part to list of upper faces
                w, h = face.shape[0], face.shape[1]
                x, y = 0, 0
                upperFace = face[y:y + round(upperFaceRatio * w), x:x + h]
                upperFaces.append(upperFace)

    print("Data prepared")
    # print total faces and labels
    print("Total full faces: ", len(fullFaces))
    print("Total upper faces: ", len(upperFaces))
    print("Total labels: ", len(labels))

    fullFaceRecogniser = cv2.face.LBPHFaceRecognizer_create()

    fullFaceRecogniser.train(fullFaces, np.array(labels))
    fullFaceRecogniser.save(fullFaceTrainerDir)
    print("Train full face recogniser successfully")

    upperFaceRecogniser = cv2.face.LBPHFaceRecognizer_create()
    upperFaceRecogniser.train(upperFaces, np.array(labels))
    upperFaceRecogniser.save(upperFaceTrainerDir)
    print("Train upper face recogniser successfully")

# retrain()


from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
prototxtPath = os.path.join(BASE_DIR, "face_detector/deploy.prototxt")
weightsPath = os.path.join(
    BASE_DIR, "face_detector/res10_300x300_ssd_iter_140000.caffemodel")
# faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
#
# # load the face mask detector model from disk
# maskNet = load_model("mask_detector.model")

def face_detect(frame, faceNet, maskNet):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                 (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            try:
                face = frame[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
                faces.append(face)
            except:
                continue

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")

        (x, y, w, h) = faces[0]
        return gray[y:y + w, x:x + h], faces[0]

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return None, None

# cap = cv2.VideoCapture(1)
#
# while True:
#     ret, image = cap.read()
#     try:
#         face, rect = face_detect(image, faceNet, maskNet)
#         (x, y, w, h) = rect
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     except:
#         pass
#     cv2.imshow('webcam', image)
#     cv2.waitKey(1)

