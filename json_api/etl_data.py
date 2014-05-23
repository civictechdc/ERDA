
#This program is meant to move data from a sqlite database into a MongoDB database.
import time

import sqlite3 as sl
from pymongo import MongoClient

#set the database bath here
#con = sl.connect('/home/ubuntu/ERDA/Data/database/EmergencyResponseData.sqlite3')
#cur = con.cursor()
#ems = cur.execute("select *, (cast(substr(response_time,3,2) as integer)*60) + cast(substr(response_time,5,2) as integer)  as response_seconds from ems where response_time < '0:30' and response_time >'0:01'")

#for row in ems:
#	print row

#map the column names for reference

#names = list(map(lambda x: x[0], ems.description))

#print names
#print ems.fetchone()


#set the mongoDB connections
mongo_con = MongoClient()
mongo_db = mongo_con.emr_db
emr_t = mongo_db.emr
#emr_t.remove()

#verify the record count
#emr_t.ensure_index("response_seconds", unique=False)
start = time.time()
#ems  = emr_t.find({"response_time":1}).sort([("response_time", 1)])

#emr_t.aggregate([
#		{'$project' : {'response_seconds':1}},
#		{'$group': {
#			'_id' : '$response_seconds',
#			'count': {'$sum':1}
#			}
#		},
#		{'$out' : 'response_seconds_freq'
#		}
#		])



#Aggregate example
emr_t.aggregate([{ '$project' : 
		{'bucket' : {'$divide' : [{'$subtract' :['$response_seconds', 
					  {'$mod': ['$response_seconds', 30]}]}, 30]
			}
		}
	}, 

	{'$group' : {
			'_id' : '$bucket',
		
			'count': {'$sum' : 1}
		}
	},

{'$out' : 'response_test'} 

])

divide_results = mongo_db.response_test

results = [x for x in divide_results.find()]
for i in results:
	print i
#key = [{'response_seconds_divide': {'$divide' : ['$response_seconds', 60]} }]
#condition = {'response_seconds_divide' : {'$gt' : 1}}
#initial = {'count' : 0}
#reduce = 'function(doc, out) {out.count++;}'



#emr_t.group(key, condition, initial, reduce)







#print keys
print time.time() - start
#load data into the database in json format - to verify data is correctly fomrated use 
#jsonlint.com

#for row in ems:
#	emr_t.insert({names[0] : row[0], names[1] : row[1], names[2] : row[2],
#			names[3] : row[3], names[4] : row[4], names[5] : row[5],
#			names[6] : row[6], names[7] : row[7], names[8] : row[8]})




