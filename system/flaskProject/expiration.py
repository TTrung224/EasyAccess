import json
from datetime import datetime
from datetime import date
import os
import pickle
import functions
from registration import uidInputHandle, uidSystemHandle, dateHandle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data/labels.pickle")
# file_path = "expire_list.txt"

with open(file_path, 'rb') as file:
    subjects = pickle.load(file)
    file.close()

date_format = "%d:%m:%Y"


# input date is a String
# input id is validated
# Function to update expire date of user
def set_expiration_time(uid, expire_time_string):
    # # process user id
    # uid = uidInputHandle(id, type)
    # if uid is False:
    #     print("uid error")
    #     return False
    
    # process user input date
    expire_time = dateHandle(expire_time_string)
    if expire_time_string is None:
        # print("date error")
        return False
    # print(uid)
    if uid not in subjects:
        return False
    else:
        subjects[uid][2] = expire_time

    with open("data/labels.pickle", 'wb') as file:
        pickle.dump(subjects, file)
        file.close()
    return True


# this function return code for each case:
# 0000: user has not been registered
# 0010: expired user
# 1: not expired yet

# *may include return time to expire date
def check_expire(id, subjects):
    # # process user id
    # uid = functions.uidHandle(id, type)
    # if uid is False:
    #     print("wrong user id format")
    #     return None

    if id not in subjects:
        return "0000"
    else:
        expire_time = subjects[id][2]
        today = date.today()
        if today > expire_time:
            return "0010"
        else:
            return "1"


# expire_time = datetime.strptime("09:08:2022", "%d:%m:%Y").date()
# set_expiration_time("3891724", expire_time)
# print(check_expire("3891724"))


def searchUser(id, type):
    uid = uidInputHandle(id, type)
    if uid is False:
        uid = ''
    try:
        info = subjects[uid]
    except Exception as e:
        return False, False, False

    id = uidSystemHandle(uid)
    return id, uid, info