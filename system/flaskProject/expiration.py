import json
from datetime import datetime
from datetime import date
import os
import pickle
import functions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "labels.pickle")
# file_path = "expire_list.txt"


with open(file_path, 'rb') as file:
    expire_time_ids = pickle.load(file)
    file.close()

date_format = "%d:%m:%Y"
# input date is a datetime object

# Function to update expire date of user
def set_expiration_time(id, expire_time):
    # process user id
    uid = functions.uidHandle(id, type)
    if uid is False:
        print("wrong user id format")
        return False

    if uid not in expire_time_ids:
        print("id not exist")
        return False
    else:
        expire_time_ids[uid][2] = expire_time

    with open("labels.pickle", 'wb') as file:
        pickle.dump(expire_time_ids, file)
        file.close()
    return True


# this function return code for each case:
# 0000: user has not been registered
# 0010: expired user
# 1: not expired yet

# *may include return time to expire date
def check_expire(id):
    # process user id
    uid = functions.uidHandle(id, type)
    if uid is False:
        print("wrong user id format")
        return None

    if uid not in expire_time_ids:
        return "0000"
    else:
        expire_time = expire_time_ids[uid][2]
        today = date.today()
        if today > expire_time:
            return "0010"
        else:
            return "1"

# expire_time = datetime.strptime("09:08:2022", "%d:%m:%Y").date()
# set_expiration_time("3891724", expire_time)
# print(check_expire("3891724"))