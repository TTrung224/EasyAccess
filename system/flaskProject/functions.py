import cv2
import os
import numpy as np
from datetime import date, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
trainerDir = os.path.join(BASE_DIR, "data/trainer.yml")

# function to detect face using OpenCV
def detect_face(img):
    # convert the test image to gray scale as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # let's detect multiscale images(some images may be closer to camera than others)
    # result is a list of faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

    # # showing the detected face followed by the waitKey method.
    # cv2.imshow("image", img)
    # cv2.waitKey(300)

    # if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None

    # under the assumption that there will be only one face,
    # extract the face area
    (x, y, w, h) = faces[0]

    # return only the face part of the image
    return gray[y:y + w, x:x + h], faces[0]


# this function will read all persons' training images, detect face from each image
# and will return two lists of exactly same size, one list
# of faces and another list of labels for each face
def prepare_training_data(data_folder_path):
    # ------STEP-1--------
    # get the directories (one directory for each subject) in data folder
    dataDirs = os.listdir(data_folder_path)

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

    # let's go through each directory and read images within it
    for dir_name in dataDirs:

        # ignore system files like .DS_Store
        if dir_name.startswith("."):
            continue

        # extract label number of subject from dir_name
        label = int(dir_name)

        # build path of directory containing images for current subject subject
        # sample subject_dir_path = "training-data/1"
        subject_dir_path = data_folder_path + "/" + dir_name

        # get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)

        # go through each image name, read image,
        # detect face and add face to list of faces
        for image_name in subject_images_names:

            # ignore system files like .DS_Store
            if image_name.startswith("."):
                continue

            # build image path
            # sample image path = training-data/1/1.pgm
            image_path = subject_dir_path + "/" + image_name

            # read image
            image = cv2.imread(image_path)

            # display an image window to show the image
            # cv2.imshow("Training on image...", image)
            # cv2.waitKey(500)

            # detect face
            face, rect = detect_face(image)

            # for the purpose of this tutorial
            # we will ignore faces that are not detected
            if face is not None:
                # add face to list of faces
                faces.append(face)
                # add label for this face
                labels.append(label)

    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return faces, labels


def train(recogniser):
    # let's first prepare our training data
    # data will be in two lists of same size
    # one list will contain all the faces
    # and the other list will contain respective labels for each face
    print("Preparing data...")
    faces, labels = prepare_training_data("training_data")
    print("Data prepared")

    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    print(labels)

    recogniser.train(faces, np.array(labels))
    recogniser.save(trainerDir)
    return recogniser


# function to draw rectangle on image
# according to given (x, y) coordinates and
# given width and height
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


# function to draw text on give image starting from
# passed (x, y) coordinates.
def draw_text(img, text, x, y):
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 2.5, 3)
    cv2.rectangle(img, (x, y), (x + w, y - (h+5)), (90, 90, 90), -1)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.5, (25, 225, 25), 3)


def predict(test_img, face_recogniser, subjects):
    # make a copy of the image as we don't want to change original image
    img = test_img.copy()

    try:
        # detect face from the image
        face, rect = detect_face(img)
        # predict the image using our face recognizer
        label, percent = face_recogniser.predict(face)
        percent = round(100 - percent)

        if percent < 60:
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, "unknown", rect[0], rect[1] - 5)
        else:
            # get name of respective label returned by face recognizer
            percent = "  {0}%".format(percent)
            label_text = subjects[str(label)][0] + " - " + percent

            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, label_text, rect[0], rect[1] - 5)
    finally:
        return img


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


def dateHandle(strDate):
    try:
        date = datetime.strptime(strDate, "%Y-%m-%d").date()
        return date
    except:
        return None
