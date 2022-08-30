import os

import cv2
from functions import detect_face

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
prototxtPath = os.path.join(BASE_DIR, "face_detector/deploy.prototxt")
weightsPath = os.path.join(
    BASE_DIR, "face_detector/res10_300x300_ssd_iter_140000.caffemodel")
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

cap = cv2.VideoCapture(1)

def getFaceImg(img):
    # convert the test image to gray scale as opencv face detector expects gray images
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5)

    if (len(faces) == 0):
        return None, None

    (x, y, w, h) = faces[0]

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
    add = 60
    x -= add
    y -= add
    w = w + (add * 2)
    h = h + (add * 2)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

    return grayImg[y:y + w, x:x + h], faces[0]

flag = True
while True:
    ret, img = cap.read()
    face, rect = detect_face(faceNet, img)
    if face is not None:
        (x, y, w, h) = rect
        h = round(0.5 * h)
        print("w x h ", w, " x ", h)
        cv2.rectangle(img, (x, y), (x + 1, y + h), (0, 255, 0), 5)
        cv2.imshow('test', face)

    if flag is True and face is not None:
        cv2.imwrite(
            "/Users/trungtran/Documents/workSpace/EasyAccess/system/flaskProject/face_training_data/testUpper" + "/" + "test" + ".jpg",
            face
        )
        flag = False
    cv2.imshow('webcam', img)

    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()