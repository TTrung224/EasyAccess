import cv2

class RecogVideo(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame = self.video.read()
        ret,jpg = cv2.imencode('.jpg',frame)
        return jpg.tobytes()

class RegisVideo(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame = self.video.read()
        ret,jpg = cv2.imencode('.jpg',frame)
        return jpg.tobytes()

class RegisWithMaskVideo(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame = self.video.read()
        ret,jpg = cv2.imencode('.jpg',frame)
        return jpg.tobytes()