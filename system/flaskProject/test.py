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



# subjects = {'13891724': ['Trung', datetime.datetime(2022, 8, 9, 23, 11, 31, 131780), datetime.date(2022, 8, 12)]}
# # subjects = {'1': 'Bill Gates', '2': 'Mark zuckerberg', '3891724': ['Trung', datetime.datetime(2022, 8, 7, 21, 7, 4, 872629), '']}
#
#
# with open("labels.pickle", 'wb') as file:
#     pickle.dump(subjects, file)
#     file.close()
#
#
# with open('labels.pickle', 'rb') as file:
#     subjects = pickle.load(file)
#     file.close()
#
# print(subjects)


