import time
import cv2
import numpy
import os
import functions
import pickle
from datetime import datetime
import expiration as expire

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataDir = os.path.join(BASE_DIR, "training_data")
dictionaryDir = os.path.join(BASE_DIR, "labels.pickle")
imageNumber = 51
adjustImageNumber = 10

def checkExist(uid):
    with open('labels.pickle', 'rb') as file:
        subjects = pickle.load(file)
        file.close()

    if uid in subjects:
        return True

    return False


# function to detect face
def getFaceImg(img):
    # convert the test image to gray scale as opencv face detector expects gray images
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # detect multiscale images
    # result is a list of faces
    faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

    # if no faces are detected then return None
    if (len(faces) == 0):
        return None, None

    # extract the face area
    (x, y, w, h) = faces[0]

    # get a bit bigger img of the face for easy further training
    add = 60
    x -= add
    y -= add
    w += add * 2
    h += add * 2

    # return only the face part of the image
    return grayImg[y:y + w, x:x + h], faces[0]


# function to write user data into pickle file
def registerGetInfo(id, name, type, expiration):
    # process user id
    uid = functions.uidHandle(id, type)
    if uid is False:
        print("wrong user id format")
        return False

    if checkExist(uid):
        print("ID existed")
        return False

    expiration = functions.dateHandle(expiration)
    if expiration is None:
        print("wrong date format")
        return False

    timeNow = datetime.now()

    # Get the subject dictionary
    with open(dictionaryDir, 'rb') as file:
        subjects = pickle.load(file)
        file.close()

    subjects[uid] = [name, timeNow, expiration]

    with open("labels.pickle", 'wb') as file:
        pickle.dump(subjects, file)
        file.close()
    return uid

# function to capture user face without mask
def registerNormalFace(uid):
    cap = cv2.VideoCapture(1)
    userDataDir = dataDir + "/" + uid
    os.mkdir(userDataDir)

    count = 1
    while True:
        ret, img = cap.read()
        face, rect = getFaceImg(img)
        cv2.imshow('webcam', img)
        cv2.waitKey(1)

        # First ten loops is for adjusting position
        if count < (adjustImageNumber + 1):
            time.sleep(0.5)
            print("1 - " + str(count))
            count += 1
            continue

        # Save face images
        if face is not None:
            print("2 - " + str(count))
            cv2.imwrite(
                userDataDir + "/" + uid + "_" + str(count - adjustImageNumber) + ".jpg",
                face
            )
            count += 1

        if count == imageNumber + adjustImageNumber:
            break
    cap.release()


# function to capture user face with mask
def registerMaskFace(uid):
    cap = cv2.VideoCapture(1)
    userDataDir = dataDir + "/" + uid

    count = imageNumber
    while True:
        ret, img = cap.read()
        face, rect = getFaceImg(img)
        cv2.imshow('webcam', img)
        cv2.waitKey(1)

        # First ten loops is for adjusting position
        if count < (adjustImageNumber + 1):
            time.sleep(0.5)
            print("1 - " + str(count))
            count += 1
            continue

        # Save face images
        if face is not None:
            print("2 - " + str(count))

            cv2.imwrite(
                userDataDir + "/" + uid + "_" + str(count - adjustImageNumber) + ".jpg",
                face
            )
            count += 1

        if count == imageNumber * 2 - 1 + adjustImageNumber:
            break

    cap.release()

    face_recogniser = cv2.face.LBPHFaceRecognizer_create()
    functions.train(face_recogniser)


# def register(id, name, type, expiration):
#     uid = registerGetInfo(id, name, type, expiration)



uid = input("id: ")
name = input("name: ")
expiration = input("expiration: ")

uid = registerGetInfo(uid, name, "student", expiration)
registerNormalFace(uid)
registerMaskFace(uid)


