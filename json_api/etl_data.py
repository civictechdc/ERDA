#This program is meant to move data from a sqlite database into a MongoDB database.


import sqlite3 as sl
from pymongo import MongoClient

#set the database bath here
con = sl.connect('EmergencyResponseData.sqlite3')
cur = con.cursor()
ems = cur.execute("select count(*)  from ems where response_time < '0:30' and response_time >'0:01'")
#map the column names for reference
names = list(map(lambda x: x[0], ems.description))

#print ems.fetchone()


#set the mongoDB connections
mongo_con = MongoClient()
mongo_db = mongo_con.emr_db
emr_t = mongo_db.emr
#emr_t.remove()

#verify the record count
#count =  emr_t.find().count()
#print count

#load data into the database in json format - to verify data is correctly fomrated use 
#jsonlint.com

for row in ems:
	emr_t.insert({names[0] : row[0], names[1] : row[1], names[2] : row[2],
			names[3] : row[3], names[4] : row[4], names[5] : row[5],
			names[6] : row[6], names[7] : row[7]})


	
