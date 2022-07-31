from gpiozero import Servo
import RPi.GPIO as GPIO
import time
import board
import busio as io
import adafruit_mlx90614
import socket
import pymysql.cursors
from datetime import datetime

GPIO.setwarnings(False)
GPIO.cleanup()

# all constant parameter goes here
PIN_NUM = 17
BASE_DEGREE = 37
SERVO_FREQ = 50

# physical pin ordering number to
# refer to the GPIO pins
GPIO.setmode(GPIO.BCM)

# set up the pin plugged and declare the servo
doorServo = Servo(PIN_NUM)
doorServo.detach()
# in servo motor,
# 1ms pulse for 0 degree (LEFT)
# 1.5ms pulse for 90 degree (MIDDLE)
# 2ms pulse for 180 degree (RIGHT)

# so for 50hz, one cycle is 20ms
# duty cycle for 0 degree = (1/20)*100 = 5%
# duty cycle for 90 degree = (1.5/20)*100 = 7.5%
# duty cycle for 180 degree = (2/20)*100 = 10%
#left_position = 0.40
#right_position = 2.5
#middle_position = (right_position - left_position) / 2 + left_position  # set the servo back to 0 degree
#ms_per_cycle = 1000 / SERVO_FREQ
# setup i2c port and mlx sensor
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

# Connect to the database
connection = pymysql.connect(host='us-cdbr-east-06.cleardb.net',
                             user='b19dfc7a972b92',
                             password='5af8fdbd',
                             database='heroku_a0c3ccec1186e2e',
                             cursorclass=pymysql.cursors.DictCursor)

def door_open():
    #duty_cycle_percentage = right_position * 100 / ms_per_cycle
    doorServo.mid()
    time.sleep(0.5)
    doorServo.detach()
    

def door_lock():
    doorServo.min()
    time.sleep(0.5)
    doorServo.detach()


def get_temperature():
    current_tem = mlx.object_temperature
    return current_tem

def insertDb(id, name):
    now = datetime.now()
    time = now.strftime("%Y/%m/%d %H:%M:%S")
    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            sql = "insert into access (personId, name, dateTime) values (%s, %s, %s)"
            cursor.execute(sql, (id, name, time))
        connection.commit()


# main program
TestFaceStatus = True
while True:
    # Testing output data for face recognition
    face_recognition = TestFaceStatus
    personId = "s1234567"
    personName = "Nguye Van A"

    obj_tem = get_temperature()

    print("temperature = " + str(obj_tem))

    if (face_recognition == True) and (obj_tem >= BASE_DEGREE):
        door_open()
        time.sleep(5)
        door_lock()
        time.sleep(2)
        insertDb(personId, personName)

    time.sleep(0.5)

