#! /usr/bin/env python
# encoding: utf-8

'''
ERDA data service API.
'''
from flask import Flask, jsonify, request, make_response, Response
import json
from pymongo import MongoClient
from bson import json_util

from werkzeug.contrib.fixers import ProxyFix

con  = MongoClient()
db = con.erda

try:
	# this is how you would normally import
	from flask.ext.cors import cross_origin
except:
	# support local usage without installed package
	from flask_cors import cross_origin

app = Flask(__name__)

#Handle Exceptions
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

class InvalidUsage(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route("/emr_data/", methods=['GET'])
@cross_origin()
#full data set api iteraion 0.1
def test():
	#returns a list of emr responses - with page  and  per_page  arguments
	
	page = int(request.args.get('page', 1))
	results_per_page = int(request.args.get('per_page', 50))
	
	lim = results_per_page
	off = 0
	
	# check if page is less then 1 or number of pages requested is 
	# out of range  - if les then 1  set page to 0 if out of range set to 
	# max range
	emr_data = db.events
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
	
	return Response(json_txt, mimetype='application/json')

#histogram iteration 0.2
@app.route("/histogram/", methods=['GET'])
@cross_origin()
def hist():
	bucket = int(request.args.get('bucket', 60))
	emr_data = db.events
	emr_data.aggregate([{ '$project' :
			{'bucket' : {'$divide' :[{'$subtract' : ['$Response Seconds',
						 {'$mod' : ['$Response Seconds', bucket]}]}, bucket]
				}
			}
			},
			{'$group' : {
					'_id' : '$bucket',
					'count' : {'$sum' : 1}
				}
			},
		{'$out' : 'hist_out'}
		])

	x = [doc for doc in db.hist_out.find()]
	json_txt = json.dumps(x, default = json_util.default)
	
	return Response(json_txt, mimetype='application/json')

@app.route("/emr_data_by_field/", methods=['GET'])
def by_field():
	emr_data = db.events
	y = emr_data.find_one()
	keys = y.keys()
	fields = request.values.getlist('field')
	field_list = []
	if len(fields) > 1:
		raise InvalidUsage('You can only select 1 feature at a time', status_code = 400)
	
	for f in keys:
		if f  in fields:
			field_list.append(f)
	
	x = [doc[field_list[0]] for doc in emr_data.find(fields = field_list)]
	
	json_txt = json.dumps(x, default = json_util.default)
	return Response(json_txt, mimetype='application/json')

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
	app.run()
