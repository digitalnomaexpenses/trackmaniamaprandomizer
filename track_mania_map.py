import requests
import re
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
import json

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/add_track', methods=['POST'])
def add_track():
	# Get the JSON data from the request
	data = request.get_json()
	
	# Extract the tags and difficulty from the data
	tags = data.get('tags')
	difficulty = data.get('difficulty')
	etags = data.get('etags')
	vehicles = data.get('vehicles')
	authorid = data.get('authorid')
	cookie = data.get('cookie')

	_tags = ''
	_difficulty = ''
	_etags = ''
	_vehicles = ''
	_authorid = ''

	if tags:
		_tags = 'tags='+tags
	if difficulty:
		_difficulty = 'difficulty='+difficulty
	if etags:
		_etags = 'etags='+etags
	if vehicles:
		_vehicles = 'vehicles='+vehicles
	if authorid:
		_authorid = 'authorid='+authorid
 
	final_string = 'https://trackmania.exchange/mapsearch2/search?random=1&'+_tags+'&'+_difficulty+'&'+_etags+'&'+_vehicles+'&'+_authorid
	final_string = re.sub(r'[&]+', '&', final_string)
	final_string = final_string.strip('&')

	url = final_string
	res = requests.get(url)
	find = re.findall(r'(?:mapdetailedinfo\?uid=[^#]{27})', res.text)

	if find:
		track_id = find[0].replace('mapdetailedinfo?uid=', '')
		print (track_id)
		post_url = 'https://trackmania.exchange/api/maps/setingamefavourite?action=add&uid='+track_id
		headers = {
			'Cookie': cookie
		}
		res = requests.post(post_url, headers=headers)
		print (res)
		if res.status_code == 200:
			return json.dumps({
				"message_code": "101",
				"message_type": "Success",
				"message": "Added Track"
			})
		else:
			return json.dumps({
				"message_code": "104",
				"message_type": "Error",
				"message": "Some Error Occured"
			})
	else:
		return json.dumps({
			"message_code": "103",
			"message_type": "Error",
			"message": "No Maps Found"
		})	

if __name__ == '__main__':
	app.run()