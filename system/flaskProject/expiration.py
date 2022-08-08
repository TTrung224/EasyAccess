import json
from datetime import datetime
from datetime import date
import os

file_path = "expire_list.txt"

f = open(file_path, "w+")
if os.stat(file_path).st_size == 0:
    json.dump({}, f)
f.close()


expire_time_ids = json.load(open(file_path))
date_format = "%d:%m:%Y"
# input date is a datetime object


def set_expiration_time(id, enter_time, expire_time):
    if id not in expire_time_ids:
        enter_time_str = enter_time.strftime(date_format)
        expire_time_str = expire_time.strftime(date_format)
        expire_time_ids[id] = "{}#{}".format(enter_time_str, expire_time_str)
    else:
        temp_str = expire_time_ids[id].split('#')
        temp_str[1] = expire_time.strftime(date_format)
        expire_time_ids[id] = "#".join(temp_str)

    json.dump(expire_time_ids, open("expire_list.txt", 'w'))


# this function return code for each case:
# 0000: user has not been registered
# 0010: expired user
# 1: not expired yet

# *may include return time to expire date
def check_expire(id):

    if id not in expire_time_ids:
        return "0000"
    else:
        expire_time_str = (expire_time_ids[id].split('#'))[1]
        expire_time = datetime.strptime(expire_time_str, date_format)
        today = datetime.strptime(datetime.strftime(
            date.today(), date_format), date_format)
        if today > expire_time:
            return "0010"
        else:
            return "1"
