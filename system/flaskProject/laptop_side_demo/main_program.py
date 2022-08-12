import requests
import json
import random
import time

dict = {'status' : False, 'ID' : '', 'name' : ''}
server_address = 'http://192.168.0.2:5000/modify_status'
server_check_address = 'http://192.168.0.2:5000/server_status_check'


n = 2
while True:

	
	print(n)
	if n > 50 and n < 80:
		dict['status'] = True
		dict['ID'] = 's3878281'
		dict['name'] = 'Vuong Viet Dung'
	try:
		s = requests.post(server_address, json=json.dumps(dict)).content
		print(s)
		while dict['status'] == True:
			respond =  requests.post(server_check_address)
			if respond.ok:
				respond = respond.json()
				print(respond['status'])
				if respond['status'] == False:
					dict = respond
				time.sleep(1)
		n = n + 5
	except requests.exceptions.ConnectionError:
		time.sleep(1)
		continue
	
	time.sleep(1)


