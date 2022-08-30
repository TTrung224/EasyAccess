from gpiozero import Servo
import time
import board
import busio as io
import adafruit_mlx90614
import pymysql.cursors
from datetime import datetime
from flask import Flask, request
import json
import requests

# address of the server
baseAddress = 'http://192.168.0.2:5000'

# all constant parameter goes here
PIN_NUM = 17
BASE_DEGREE = 35
SICK_DEGREE = 37
SERVO_FREQ = 50
TEMPERATURE_TIMES = 26
TEMPERATURE_REMOVE = 3

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
# middle_position = (right_position - left_position) / 2 + left_position  # set the servo back to 0 degree
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


def insertDb(id, name):
    now = datetime.now()
    time = now.strftime("%Y/%m/%d %H:%M:%S")
    connection.ping()
    with connection:
        with connection.cursor() as cursor:
            sql = "insert into access (personId, name, dateTime) values (%s, %s, %s)"
            cursor.execute(sql, (id, name, time))
        connection.commit()


def avg_temperature():
    obj_tem = []
    avg_obj_tem = 0

    for i in range(0, TEMPERATURE_TIMES):
        obj_tem.append(mlx.object_temperature)

    sorted(obj_tem)

    for k in range(TEMPERATURE_REMOVE, TEMPERATURE_TIMES - TEMPERATURE_REMOVE):
        avg_obj_tem += obj_tem[k]
        # avg_amb_tem += amb_tem[k]
    avg_obj_tem = avg_obj_tem / (TEMPERATURE_TIMES - (TEMPERATURE_REMOVE*2))
    return avg_obj_tem

# flask configuration


# main program
server_address = baseAddress + '/status_send'
server_reset_address = baseAddress + '/reset_status'
server_door_modify_address = baseAddress + '/modify_door_status'
server_temp_modify_address = baseAddress + '/modify_temp'

# respond = {"status": False, "name": "", "ID": ""}

while True:
    try:
        respond = requests.post(server_address, json={"mytext": "lalala"})
        if respond.ok:
            print(respond.json())
            respond = respond.json()
            TestFaceStatus = respond['status']
        time.sleep(.2)

    except requests.exceptions.ConnectionError:
        time.sleep(.2)
        continue

    # Testing output data for face recognition
    face_recognition = respond["status"]
    personId = respond['ID']
    personName = respond['name']

    obj_tem = round(avg_temperature(),1)
    try:
        dict_holder = {'temp': obj_tem}
        res = requests.post(server_temp_modify_address, json=json.dumps(dict_holder))
        if res.ok:
            print(res.content.decode("utf-8"))
    except requests.exceptions.ConnectionError:
        pass

    print("temperature = " + str(obj_tem))

    # remember to change condition when demo
    if (face_recognition == True) and (obj_tem > BASE_DEGREE) and (obj_tem < SICK_DEGREE):
        door_open()
        try:
            dict_holder = {"door": True}
            res = requests.post(server_door_modify_address, json=json.dumps(dict_holder))
            if res.ok:
                print(res.content.decode("utf-8"))
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(5)
        door_lock()
        try:
            dict_holder = {"door": False}
            res = requests.post(server_door_modify_address, json=json.dumps(dict_holder))
            if res.ok:
                print(res.content.decode("utf-8"))
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
        insertDb(personId, personName)


    # resetting status
    try:
        res = requests.get(server_reset_address)
        if res.ok:
            print(res.content.decode("utf-8"))
        time.sleep(.2)
    except requests.exceptions.ConnectionError:
        pass