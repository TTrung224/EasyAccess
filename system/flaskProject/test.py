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
# subjects = {'13852304': ['Thong Doan', datetime.datetime(2022, 9, 13, 18, 47, 6, 716489), datetime.date(2022, 10, 1)]}
#
# with open("data/labels.pickle", 'wb') as file:
#     pickle.dump(subjects, file)
#     file.close()
#
#
# with open('data/labels.pickle', 'rb') as file:
#     subjects = pickle.load(file)
#     file.close()

# a = subjects['13891724'][2]
# print(subjects)
# print(a)


"""****************"""
from functions import detect_face
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
faceTrainingDataDir = os.path.join(BASE_DIR, "face_training_data")
dictionaryDir = os.path.join(BASE_DIR, "data/labels.pickle")
fullFaceTrainerDir = os.path.join(BASE_DIR, "data/fullFaceTrainer.yml")
upperFaceTrainerDir = os.path.join(BASE_DIR, "data/upperFaceTrainer.yml")
upperFaceRatio = 0.6

prototxtPath = os.path.join(BASE_DIR, "face_detector/deploy.prototxt")
weightsPath = os.path.join(
    BASE_DIR, "face_detector/res10_300x300_ssd_iter_140000.caffemodel")
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

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
            face, rect = detect_face(faceNet, image)

            if face is not None:
                # add label for this face
                labels.append(label)

                # add face to list of faces
                fullFaces.append(face)

                # add upper face part to list of upper faces
                w, h = face.shape[0], face.shape[1]
                x, y = 0, 0
                upperFace = face[y:y + round(upperFaceRatio * h), x:x + w]
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
