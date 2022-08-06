"""'
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition

Developed by ThgDoan
"""

import cv2
import os
from datetime import datetime

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video width
cam.set(4, 480)  # set video height

# face_detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# For each person, enter one numeric face id
face_id = input("\n enter user id ==>  ")


def current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


print(
    "\n [INFO] ["
    + current_time()
    + "] Initializing face capture. Look at the camera and wait ..."
)
# Initialize individual sampling face count
count = 0

while True:

    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite(
            "EasyAccess/dataset/User." +
            str(face_id) + "." + str(count) + ".jpg",
            gray[y: y + h, x: x + w],
        )

        cv2.imshow("image", img)

    k = cv2.waitKey(100) & 0xFF  # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30:  # Take 30 face sample and stop the video
        break

now = datetime.now()
# Do a bit of cleanup
print("\n [INFO] [" + current_time() + "] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
