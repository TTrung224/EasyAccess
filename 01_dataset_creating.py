import cv2
import os
from datetime import datetime


def current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


# def face_capture(name) expected to return num of img (web app)

# For each person, enter one numeric face id
name = input("\n enter user name ==>  ")
print(
    "\n [INFO] ["
    + current_time()
    + "] Initializing face capture. Look at the camera and wait ..."
)
path = "EasyAccess/dataset/" + name
# Initialize individual sampling face count
num_of_images = 0
# face_detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

try:
    os.makedirs(path)
except:
    print('Directory Already Created')
cam = cv2.VideoCapture(0)
# cam.set(3, 640)  # set video width
# cam.set(4, 480)  # set video height

while True:
    ret, img = cam.read()
    new_img = None
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        image=gray_img, scaleFactor=1.3, minNeighbors=5)
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img, "Face Detected", (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
        cv2.putText(img, str(str(num_of_images)+" images captured"),
                    (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
        new_img = gray_img[y:y+h, x:x+w]
    cv2.imshow("FaceDetection", img)
    key = cv2.waitKey(1) & 0xFF
    # Save the captured image into the datasets folder
    try:
        cv2.imwrite(str(path+"/"+ name +
                    "." + str(num_of_images) + ".jpg"), new_img)
        num_of_images += 1
    except:
        pass
    # if key == ord("q") or key == 27 or num_of_images > 10:  # Take 30 face sample and stop the video
    #     break
    k = cv2.waitKey(100) & 0xFF  # Press 'ESC' for exiting video
    if k == 27:
        break
    elif num_of_images >= 10:  # Take 10 face sample and stop the video
        break
now = datetime.now()
# Do a bit of cleanup
print("\n [INFO] [" + current_time() + "] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
# cv2.destroyAllWindows()
# return num_of_images
