import requests
import json
import time

status = False


while True:
	try:
		respond = requests.post(server_address, json={"mytext":"lalala"})
		if respond.ok:
			print(respond.json())
		time.sleep(1)
		
		print("resetting status")
		res = requests.get(server_reset_address)
		if res.ok:
			print(res.content.decode("utf-8"))
		time.sleep(1)
	except:
		print()
	finally:
		print("the program finished")
		time.sleep(1)
# while True:
# 	import requests
# 	res = requests.post('http://192.168.0.2:5000/api/add_message/1234', json={"mytext":"lalala"})
# 	if res.ok:
# 	    print(res.json())
# 	time.sleep(3)
