import cv2
import os

import numpy as np

from functions import detect_face, draw_text
import pickle
from datetime import datetime, timedelta

# directories of the system files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
faceTrainingDataDir = os.path.join(BASE_DIR, "face_training_data")
dictionaryDir = os.path.join(BASE_DIR, "data/labels.pickle")
fullFaceTrainerDir = os.path.join(BASE_DIR, "data/fullFaceTrainer.yml")
upperFaceTrainerDir = os.path.join(BASE_DIR, "data/upperFaceTrainer.yml")

prototxtPath = os.path.join(BASE_DIR, "face_detector/deploy.prototxt")
weightsPath = os.path.join(
    BASE_DIR, "face_detector/res10_300x300_ssd_iter_140000.caffemodel")
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# number of training image per person
realImageNumber = 200
imageNumber = realImageNumber + 1

# number of loops before taking training image
adjustImageNumber = 20

upperFaceRatio = 0.5

# function to train the fullFace recogniser


def trainFaceData(uid):
    print("face data train:")
    print("Preparing data...")

    # list to hold all subject faces
    fullFaces = []

    # list to hold all subject upper faces
    upperFaces = []

    # list to hold labels for all subjects
    labels = []

    userDir = faceTrainingDataDir + "/" + uid

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
        face, rect = detect_face(faceNet, image)

        if face is not None:
            # add label for this face
            labels.append(label)

            # add face to list of full faces
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

    if len(labels) > 0:
        fullFaceRecogniser = cv2.face.LBPHFaceRecognizer_create()
        if os.path.exists(fullFaceTrainerDir):
            fullFaceRecogniser.read(fullFaceTrainerDir)
            fullFaceRecogniser.update(fullFaces, np.array(labels))
            fullFaceRecogniser.save(fullFaceTrainerDir)
        else:
            fullFaceRecogniser.train(fullFaces, np.array(labels))
            fullFaceRecogniser.save(fullFaceTrainerDir)
        print("Train full face recogniser successfully")

        upperFaceRecogniser = cv2.face.LBPHFaceRecognizer_create()
        if os.path.exists(upperFaceTrainerDir):
            upperFaceRecogniser.read(upperFaceTrainerDir)
            upperFaceRecogniser.update(upperFaces, np.array(labels))
            upperFaceRecogniser.save(upperFaceTrainerDir)
        else:
            upperFaceRecogniser.train(upperFaces, np.array(labels))
            upperFaceRecogniser.save(upperFaceTrainerDir)
        print("Train upper face recogniser successfully")
    else:
        print("train failed")

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
    # # convert the test image to gray scale as opencv face detector expects gray images
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # # load OpenCV face detector
    # face_cascade = cv2.CascadeClassifier(
    #     cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    #
    # # detect multiscale images
    # # result is a list of faces
    # faces = face_cascade.detectMultiScale(
    #     grayImg, scaleFactor=1.1, minNeighbors=5)
    #
    # # if no faces are detected then return None
    # if (len(faces) == 0):
    #     return None, None
    #
    # # extract the face area
    # (x, y, w, h) = faces[0]

    face, rect = detect_face(faceNet, img)
    (x, y, w, h) = rect

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
    add = 60
    x -= add
    y -= add
    w += add * 2
    h += add * 2
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

    # add = 60
    # x -= add
    # y -= add
    # w += add * 2
    # h += add * 2

    # return only the face part of the image
    return grayImg[y:y + h, x:x + w], rect


# function to get training upper part face image
def getUpperFaceImg(img):
    # convert the test image to gray scale as opencv face detector expects gray images
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # # load OpenCV face detector
    # face_cascade = cv2.CascadeClassifier(
    #     cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    #
    # # detect multiscale images
    # # result is a list of faces
    # faces = face_cascade.detectMultiScale(
    #     grayImg, scaleFactor=1.1, minNeighbors=5)

    face, rect = detect_face(faceNet, img)

    # if no faces are detected then return None
    if face is None:
        return None, None

    # extract the face area
    (x, y, w, h) = rect

    height = round(upperFaceRatio * h)
    cv2.rectangle(img, (x, y), (x + w, y + height), (0, 255, 0), 5)

    # return the upper face part of the image
    return grayImg[y:y + round(upperFaceRatio * w), x:x + h], rect


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


# function to capture user face
def registerFace(uid, image_hub):
    # cap = cv2.VideoCapture(1)
    userFaceDataDir = faceTrainingDataDir + "/" + uid
    os.mkdir(userFaceDataDir)

    count = 1
    while True:
        flag = True
        # ret, img = cap.read()
        try:
            rpi_name, img = image_hub.recv_image()
            image_hub.send_reply(b'OK')
            if img is None:
                continue
        except Exception:
            continue

        face, rect = getFaceImg(img)

        # First loops is for adjusting position
        if count < (adjustImageNumber + 1):
            # print("1 - " + str(count))
            count += 1
            flag = False

        # Save fullFace and upperFace images
        if face is not None and flag is True:
            # print("2 - " + str(count))
            try:
                cv2.imwrite(
                    userFaceDataDir + "/" + uid + "_" +
                    str(count - adjustImageNumber) + ".jpg",
                    face
                )
            except:
                continue
            count += 1
            finishPercent = round(
                (count - adjustImageNumber) / imageNumber * 100)
            draw_text(img, str(finishPercent) + "%", rect[0], rect[1] - 5)

        ret, jpg = cv2.imencode('.jpg', img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() +
               b'\r\n\r\n')

        if count == imageNumber + adjustImageNumber:
            break

    # cap.release()
    trainFaceData(uid)

# def register(id, name, type, expiration):
#     uid = registerGetInfo(id, name, type, expiration)


# uid = input("id: ")
# name = input("name: ")
# expiration = input("expiration: ")
#
# uid = registerGetInfo(uid, name, "student", expiration)
# registerNormalFace("12")
# registerMaskFace("12")
