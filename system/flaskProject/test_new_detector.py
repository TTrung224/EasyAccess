import numpy as np
import imutils
import time
from tensorflow.keras.models import load_model
import cv2
from imutils.video import VideoStream
import os
import pickle
import detect_mask_video
from registration import getUpperFaceImg
from registration import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dictionaryDir = os.path.join(BASE_DIR, "data/labels.pickle")
fullFaceTrainerDir = os.path.join(BASE_DIR, "data/fullFaceTrainer.yml")
upperFaceTrainerDir = os.path.join(BASE_DIR, "data/upperFaceTrainer.yml")
faceTrainingDataDir = os.path.join(BASE_DIR, "face_training_data")
maskNet = load_model(os.path.join(BASE_DIR, "mask_detector.model"))
realImageNumber = 200
imageNumber = realImageNumber + 1

# number of loops before taking training image
adjustImageNumber = 20

upperFaceRatio = 0.5

prototxtPath = os.path.join(BASE_DIR, "face_detector/deploy.prototxt")
weightsPath = os.path.join(
    BASE_DIR, "face_detector/res10_300x300_ssd_iter_140000.caffemodel")
net = cv2.dnn.readNetFromCaffe(prototxtPath, weightsPath)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# function to draw a rectangle around an object


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (w, h), (0, 255, 0), 2)


# function to add text to a rectangle
def draw_text(img, text, x, y):
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 2.5, 3)

    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN,
                2.5, (25, 225, 25), 3)


# function to detect existence of people face
# def detect_face(img):
#     # convert the test image to gray scale as opencv face detector expects gray images
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # load OpenCV face detector
#     face_cascade = cv2.CascadeClassifier(
#         cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#     faces = face_cascade.detectMultiScale(
#         gray, scaleFactor=1.1, minNeighbors=5)

#     # for x, y, w, h in faces:
#     #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

#     # if no faces are detected then return original img
#     if (len(faces) == 0):
#         return None, None

#     # under the assumption that there will be only one face,
#     # extract the face area
#     (x, y, w, h) = faces[0]

#     # return only the face part of the image
#     return gray[y:y + w, x:x + h], faces[0]


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

print("[INFORMATion] Starting Video Stream ...")
video_capture = cv2.VideoCapture(0)
time.sleep(2)


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
            box.append([x1, y1, x2, y2])
            top = x1
            right = y1
            bottom = x2-x1
            left = y2-y1

            #  blurry rectangle to the detected face
            face = frame[right:right+left, top:top+bottom]
            frame[right:right+face.shape[0], top:top+face.shape[1]] = face

    return gray[x1:x1+x2, y1:y1+y2], tuple(box[0])

# while True:
# 	frame = vs.read()

# 	#grab frame dims  and convert it to a blob
# 	(h, w) = frame.shape[: 2]
# 	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300,300)), 1.0, (300,300), (104.0, 177.0, 123.0))
# 	faceNet.setInput(blob)
# 	detections = faceNet.forward()

# 	#loop over detections

# 	for i in range (0, detections.shape[2]):
# 		#extract confidence
# 		confidence = detections[0, 0, i, 2]
# 		if confidence > 0.7:
# 		# comute x and y
# 			box = detections[0, 0, i, 3:7] * np.array([w,h,w,h])
# 			(startX, startY, endX, endY) = box.astype("int")

# 			#draw the bounding boxes
# 			text = "{:2f}%".format(confidence * 100)
# 			y = startY - 10 if startY - 10 > 10 else startY + 10
# 			# cv2.rectangle(frame, (startX, startY), (endX, endY), (0,0,225), 2)
# 			confidence = f'{confidence*100}'
# 			draw_rectangle(frame, (startX, startY, endX, endY))
# 			draw_text(frame, confidence, startX, startY)

# 	cv2.imshow("Frame", frame)
# 	key = cv2.waitKey(1) & 0xFF

# 			#if 'q' button is press -> quit
# 	if key == ord("q"):
# 		break
# cv2.destroyAllWindows()
# vs.stop()


def predict(test_img, face_recogniser, subjects):
    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    try:
        # detect face from the image
        face, rect = detect_face(img, net)
        # predict the image using our face recognizer
        label, percent = face_recogniser.predict(face)
        percent = round(100 - percent)
        # print(label, percent)

        if percent < 50:
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, "unknown", rect[0], rect[1] - 5)
        else:
            # get name of respective label returned by face recognizer
            percent = "{0}%".format(percent)
            # label_text = subjects[str(label)][0] + " - " + percent
            label_text = subjects[str(label)][0]
            dict_holder = {"status": True, "ID": str(
                label), "name": subjects[str(label)][0]}
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, label_text, rect[0], rect[1] - 5)
    finally:
        return img


def getFaceImg(frame):
    # convert the test image to gray scale as opencv face detector expects gray images
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
        if confidence > 0.7:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            box.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0),
                          int(round(frameHeight / 150)), 8,)
            top = x1
            right = y1
            bottom = x2-x1
            left = y2-y1

            #  blurry rectangle to the detected face
            face = frame[right:right+left, top:top+bottom]
            frame[right:right+face.shape[0], top:top+face.shape[1]] = face

    # get a bit bigger img of the face for easy further training
    add = 60
    x1 -= add
    y1 -= add
    x2 += add * 2
    y2 += add * 2

    # return only the face part of the image
    return gray[x1:x1+x2, y1:y1+y2], tuple(box[0])


def upperFacePredict(test_img, face_recogniser, subjects):
    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    try:
        # detect face from the image
        face, rect = getUpperFaceImg(img)
        # predict the image using our face recognizer
        label, percent = face_recogniser.predict(face)
        percent = round(100 - percent)
        # print(label, percent)

        if percent < 40:
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, "unknown", rect[0], rect[1] - 5)
        else:
            # get name of respective label returned by face recognizer
            percent = "{0}%".format(percent)
            # label_text = subjects[str(label)][0] + " - " + percent
            label_text = subjects[str(label)][0]
            dict_holder = {"status": True, "ID": str(
                label), "name": subjects[str(label)][0]}
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, label_text, rect[0], rect[1] - 5)
    finally:
        return img


def registerFace(uid, frame):
    # cap = cv2.VideoCapture(1)
    userFaceDataDir = faceTrainingDataDir + "/" + uid
    os.mkdir(userFaceDataDir)

    count = 1
    while True:
        flag = True
        # ret, img = cap.read()
        try:
            img = frame
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


# main function to recognise people
def recognise(frame):
    with open(dictionaryDir, 'rb') as file:
        subjects = pickle.load(file)
        file.close()

    # create our LBPH face recognizer
    face_recogniser = cv2.face.LBPHFaceRecognizer_create()
    upper_face_recogniser = cv2.face.LBPHFaceRecognizer_create()
    face_recogniser.read(fullFaceTrainerDir)
    upper_face_recogniser.read(upperFaceTrainerDir)
    # face_recogniser = functions.train(face_recogniser)
    # cap = cv2.VideoCapture(1)

    while True:
        # ret, img = cap.read()
        try:
            img = frame
            if img is None:
                continue
        except Exception:
            continue

        detect_result = detect_mask_video.mask_detector(img, net, maskNet)
        print(detect_result)
        if detect_result is True:
            img = upperFacePredict(img, upper_face_recogniser, subjects)
            ret, jpg = cv2.imencode('.jpg', img)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() +
                   b'\r\n\r\n')
        else:
            img = predict(img, face_recogniser, subjects)
            ret, jpg = cv2.imencode('.jpg', img)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() +
                   b'\r\n\r\n')


# detectionEnabled = False
# while True:
#     _, frameOrig = video_capture.read()
#     frame = frameOrig

#     if(detectionEnabled == True):
#         outOpencvDnn, box = detectFaceOpenCVDnn(net, frame)

#     cv2.imshow('Frame', frame)

#     # key controller
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord("d"):
#         detectionEnabled = not detectionEnabled

#     if key == ord("q"):
#         break

# video_capture.release()
# cv2.destroyAllWindows( )
while True:

    _, frame = video_capture.read()
    registerFace("s3878281", frame)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
