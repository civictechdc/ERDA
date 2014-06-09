#! /usr/bin/env python
# encoding: utf-8

'''
Imports a CSV file, containing DC emergency response data, to MongoDB.
'''
import sys
import csv
import time
from pymongo import MongoClient

def import_erda_csv(file_name):
	print(file_name)
	start = time.time()
	data = []
	with open(file_name, 'r') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			data.append(row)
		elapsed = '{:2.2f}'.format(time.time() - start)
		print('Read', len(data) - 1, 'records in', elapsed, 's')
	return data
def make_seconds(hh_mm_ss):
	try:
		return int(hh_mm_ss[3:5])* 60 + int(hh_mm_ss[6:8])
	except:
		print format('bad data : ' + hh_mm_ss)
		pass


def init_db(data):
	print('Creating database tables...')
	start = time.time()
	mongo_con = MongoClient()
	erda_db = mongo_con.erda
	events_collection = erda_db.events
	events_collection.remove()
	events = iter(data)
	header = next(events)
	for event in events:
		
		events_collection.insert({
			header[0] : event[0], header[1] : event[1], header[2] : event[2],
			header[3] : event[3], header[4] : event[4], header[5] : event[5], 
			'Response Seconds' : make_seconds(event[4])
		})
	elapsed = '{:2.2f}'.format(time.time() - start)
	print('Imported', len(data) - 1, 'records in', elapsed, 's')

def usage():
	'''Prints a help string.'''
	print("usage: import.py <filename>")

if __name__ == "__main__":
	if (len(sys.argv) == 2):
		init_db(import_erda_csv(sys.argv[1]))
	else:
		usage()
