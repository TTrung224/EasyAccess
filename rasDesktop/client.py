# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import socket
import time
import os

ipFile = "/home/pi/Desktop/ip.txt"

if os.path.exists(ipFile):
	# address of the server
	file = open(ipFile, 'r')
	baseAddress = 'tcp://' + file.read().strip() + ":5555"
	file.close()
else:
    ip = input("Server IP address: ")
    baseAddress = 'tcp://' + ip + ":5555"
    f = open(ipFile, "w")
    f.write(ip)
    f.close()

print("Server IP address: " + baseAddress)
print("streaming")

# baseAddress = "tcp://192.168.2.248:5555"

# initialize the ImageSender object with the socket address of the server
sender = imagezmq.ImageSender(connect_to = baseAddress)

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0, resolution=(1024, 768)).start()
time.sleep(2.0)

while True:
	# read the frame from the camera and send it to the server
	frame = vs.read()
	sender.send_image(rpiName, frame)