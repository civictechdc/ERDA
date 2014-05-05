from flask import Flask, jsonify, request, make_response
import json
from pymongo import MongoClient
from bson import json_util

from werkzeug.contrib.fixers import ProxyFix

con  = MongoClient()
db = con.emr_db

try:
    # this is how you would normally import
    from flask.ext.cors import cross_origin
except:
    # support local usage without installed package
    from flask_cors import cross_origin

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/emr_data/", methods=['GET'])
@cross_origin()
def test():
	#returns a list of emr responses - with limit and offset arguments
	
	page = int(request.args.get('page', 1))
	results_per_page = int(request.args.get('per_page', 50))
	
	lim = results_per_page
	off = 0
	
	# check if page is less then 1 or number of pages requested is 
	# out of range  - if les then 1  set page to 0 if out of range set to 
	# max range
	emr_data = db.emr
	count = emr_data.find().count()
	#set the maximum results per page at 1000
	if results_per_page > 1000:
		results_per_page = 1000
		
	#find the maximum number of pages given the results_per_page size	
	max_page = (count / results_per_page)
	
	if page > max_page:
		page = max_page
		
	if page < 1:
		off = 0
	else:
		off = results_per_page * (page - 1)

	
	x = [doc for doc in emr_data.find().skip(off).limit(lim)]
	json_txt = json.dumps(x, default = json_util.default)
	
	return json_txt
	

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
	app.run()
