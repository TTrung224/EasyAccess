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
# # subjects = {'13891724': ['Trung', datetime.datetime(2022, 8, 9, 23, 11, 31, 131780), datetime.date(2022, 8, 12)]}
# # subjects = {'1': 'Bill Gates', '2': 'Mark zuckerberg', '3891724': ['Trung', datetime.datetime(2022, 8, 7, 21, 7, 4, 872629), '']}
#
#
# # with open("data/labels.pickle", 'wb') as file:
# #     pickle.dump(subjects, file)
# #     file.close()
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
fullFaceTrainingDataDir = os.path.join(BASE_DIR, "fullFace_training_data")
upperFaceTrainingDataDir = os.path.join(BASE_DIR, "upperFace_training_data")
dictionaryDir = os.path.join(BASE_DIR, "data/labels.pickle")
fullFaceTrainerDir = os.path.join(BASE_DIR, "data/fullFaceTrainer.yml")
upperFaceTrainerDir = os.path.join(BASE_DIR, "data/upperFaceTrainer.yml")


def retrainFull():
    print("full face train:")
    print("Preparing data...")

    dataDirs = os.listdir(fullFaceTrainingDataDir)

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

    for dirName in dataDirs:

        # ignore system files like .DS_Store
        if dirName.startswith("."):
            continue

        # extract label number of subject from dir_name
        label = int(dirName)

        userDir = fullFaceTrainingDataDir + "/" + dirName
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
                # add face to list of faces
                faces.append(face)
                # add label for this face
                labels.append(label)

    print("Data prepared")
    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))

    recogniser = cv2.face.LBPHFaceRecognizer_create()
    recogniser.train(faces, np.array(labels))
    recogniser.save(fullFaceTrainerDir)
    print("Train fullFace successfully")


def retrainUpper():
    print("upper face train:")
    print("Preparing data...")

    dataDirs = os.listdir(upperFaceTrainingDataDir)

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

    for dirName in dataDirs:

        # ignore system files like .DS_Store
        if dirName.startswith("."):
            continue

        # extract label number of subject from dir_name
        label = int(dirName)

        userDir = upperFaceTrainingDataDir + "/" + dirName
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

            # add face to list of faces
            faces.append(image)
            # add label for this face
            labels.append(label)

    print("Data prepared")
    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))

    recogniser = cv2.face.LBPHFaceRecognizer_create()
    recogniser.train(faces, np.array(labels))
    recogniser.save(upperFaceTrainerDir)
    print("Train upperFace successfully")


# retrainFull()
# retrainUpper()