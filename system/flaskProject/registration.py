import cv2
import os

import numpy as np

from functions import detect_face, draw_text
import pickle
from datetime import datetime, timedelta

# directories of the system files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
fullFaceTrainingDataDir = os.path.join(BASE_DIR, "fullFace_training_data")
upperFaceTrainingDataDir = os.path.join(BASE_DIR, "upperFace_training_data")
dictionaryDir = os.path.join(BASE_DIR, "data/labels.pickle")
fullFaceTrainerDir = os.path.join(BASE_DIR, "data/fullFaceTrainer.yml")
upperFaceTrainerDir = os.path.join(BASE_DIR, "data/upperFaceTrainer.yml")

# number of training image per person
realImageNumber = 200
imageNumber = realImageNumber + 1

# number of loops before taking training image
adjustImageNumber = 20

upperFaceRatio = 0.5

# function to train the fullFace recogniser


def trainFullFace(uid):
    print("full face train:")
    print("Preparing data...")

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

    userDir = fullFaceTrainingDataDir + "/" + uid

    label = int(uid)

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
    if os.path.exists(fullFaceTrainerDir):
        recogniser.read(fullFaceTrainerDir)
        recogniser.update(faces, np.array(labels))
        recogniser.save(fullFaceTrainerDir)
    else:
        recogniser.train(faces, np.array(labels))
        recogniser.save(fullFaceTrainerDir)
    print("Train fullFace successfully")


# function to train the upperFace recogniser
def trainUpperFace(uid):
    print("upper face train:")
    print("Preparing data...")

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

    userDir = upperFaceTrainingDataDir + "/" + uid

    label = int(uid)

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
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # add face to list of faces
        faces.append(img)
        # add label for this face
        labels.append(label)

    print("Data prepared")
    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))

    recogniser = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(upperFaceTrainerDir):
        recogniser.read(upperFaceTrainerDir)
        recogniser.update(faces, np.array(labels))
        recogniser.save(upperFaceTrainerDir)
    else:
        recogniser.train(faces, np.array(labels))
        recogniser.save(upperFaceTrainerDir)
    print("Train upperFace successfully")


# function to handle the user id input
def uidHandle(uid, type):
    try:
        int(uid[0])
    except:
        uid = uid[1:]

    if type == "student":
        uid = "1" + uid
    elif type == "staff":
        uid = "2" + uid
    elif type == "visitor":
        uid = "3" + uid
    else:
        return False
    return uid


# function to handle the user string date input
def dateHandle(strDate):
    try:
        date = datetime.strptime(strDate, "%Y-%m-%d").date()
        return date
    except:
        return None


# function to check the existence of an user id
def checkExist(uid):
    with open('data/labels.pickle', 'rb') as file:
        subjects = pickle.load(file)
        file.close()

    if uid in subjects:
        return True

    return False


# function to get training face image
def getFaceImg(img):
    # convert the test image to gray scale as opencv face detector expects gray images
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # detect multiscale images
    # result is a list of faces
    faces = face_cascade.detectMultiScale(
        grayImg, scaleFactor=1.1, minNeighbors=5)

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


# function to get training upper part face image
def getUpperFaceImg(img):
    # convert the test image to gray scale as opencv face detector expects gray images
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # detect multiscale images
    # result is a list of faces
    faces = face_cascade.detectMultiScale(
        grayImg, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in faces:
        height = round(upperFaceRatio * h)
        cv2.rectangle(img, (x, y), (x + w, y + height), (0, 255, 0), 5)

    # if no faces are detected then return None
    if (len(faces) == 0):
        return None, None

    # extract the face area
    (x, y, w, h) = faces[0]

    # return the upper face part of the image
    return grayImg[y:y + round(upperFaceRatio * w), x:x + h], faces[0]


# function to write user data into pickle file
def registerGetInfo(id, name, type, expiration):
    # process user id
    uid = uidHandle(id, type)
    if uid is False:
        print("wrong user id format")
        return "wrong-id"

    if checkExist(uid):
        print("ID existed")
        return "existed"

    expiration = dateHandle(expiration)
    if expiration is None:
        print("wrong date format")
        return "wrong-date"

    timeNow = datetime.now()
    if type == "visitor":
        expiration = timeNow.date() + timedelta(days=1)

    # Get the subject dictionary
    with open(dictionaryDir, 'rb') as file:
        subjects = pickle.load(file)
        file.close()

    subjects[uid] = [name, timeNow, expiration]

    with open("data/labels.pickle", 'wb') as file:
        pickle.dump(subjects, file)
        file.close()
    return uid


# function to capture user face without mask
def registerFace(uid, image_hub):
    # cap = cv2.VideoCapture(1)
    userFullFaceDataDir = fullFaceTrainingDataDir + "/" + uid
    os.mkdir(userFullFaceDataDir)
    userUpperFaceDataDir = upperFaceTrainingDataDir + "/" + uid
    os.mkdir(userUpperFaceDataDir)

    count = 1
    while True:
        flag = True
        # ret, img = cap.read()
        rpi_name, img = image_hub.recv_image()
        if img is None:
            continue
        image_hub.send_reply(b'OK')

        face, rect = getFaceImg(img)
        upperFace, upperRect = getUpperFaceImg(img)

        # First loops is for adjusting position
        if count < (adjustImageNumber + 1):
            # print("1 - " + str(count))
            count += 1
            flag = False

        # Save fullFace and upperFace images
        if face is not None and upperFace is not None and flag is True:
            # print("2 - " + str(count))
            try:
                cv2.imwrite(
                    userFullFaceDataDir + "/" + uid + "_" +
                    str(count - adjustImageNumber) + ".jpg",
                    face
                )
                cv2.imwrite(
                    userUpperFaceDataDir + "/" + uid + "_" +
                    str(count - adjustImageNumber) + ".jpg",
                    upperFace
                )
            except:
                continue
            count += 1
            finishPercent = round((count - adjustImageNumber) / imageNumber * 100)
            draw_text(img, str(finishPercent) + "%", rect[0], rect[1] - 5)

        ret, jpg = cv2.imencode('.jpg', img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() +
               b'\r\n\r\n')

        if count == imageNumber + adjustImageNumber:
            break

    # cap.release()
    trainFullFace(uid)
    trainUpperFace(uid)


# def register(id, name, type, expiration):
#     uid = registerGetInfo(id, name, type, expiration)


# uid = input("id: ")
# name = input("name: ")
# expiration = input("expiration: ")
#
# uid = registerGetInfo(uid, name, "student", expiration)
# registerNormalFace("12")
# registerMaskFace("12")
