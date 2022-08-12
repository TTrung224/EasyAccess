from flask import Flask, request, jsonify
import json


dict = {'status' : False, 'ID' : '', 'name' : ''}

app = Flask(__name__)
@app.route('/status_send', methods = ['POST'])
def status_send():
	result = dict
	return jsonify(result)

@app.route('/reset_status', methods = ['POST', 'GET'])
def reset_status():
	dict['status'] = False
	dict['ID'] = ''
	dict['name'] = ''
	return "reset done"

#modify status when main program recognize faces
@app.route('/modify_status', methods = ['POST'])
def modify_status():
	jsondata = request.get_json()
	data = json.loads(jsondata)
	dict['status'] = True
	dict['ID'] = data['ID']
	dict['name'] = data['name']
	return "message received"
	
#to check status sent from main program
@app.route('/server_status_check', methods = ['POST'])
def server_status_check():
	return jsonify(dict)
	
	
	
if __name__ == '__main__':
	app.run(debug=False)





"""
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print(content['mytext'])
    return jsonify({"uuid":uuid})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)"""
