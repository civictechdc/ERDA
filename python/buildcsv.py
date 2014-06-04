#! /usr/bin/env python
# encoding: utf-8

'''
Converts and merges multiple .xlsx Excel files containing DC emergency response
data into a single .csv file.
'''
import sys
import glob
from collections import defaultdict, OrderedDict
import pandas as pd
import csv

def address_quadrant(address):
	'''Parses out the quadrant from an address string, if it contains one.'''
	quad = address.strip().split(' ')
	if 'NW' in quad:
		return 'NW'
	elif 'NE' in quad:
		return "NE"
	elif 'SW' in quad:
		return 'SW'
	elif 'SE' in quad:
		return 'SE'
	else:
		return 'NA'

def normalize_address(address):
	return address.strip().upper()

def print_summary(num_valid, errors):
	num_no_address = sum(e[0] == 'no address' for e in errors)
	num_blank_address = sum(e[0] == 'blank address' for e in errors)
	print(num_valid, 'valid incident(s) processed.')
	print(len(errors), 'incident(s) were excluded:')
	print(num_no_address, 'incident(s) had an empty address field.')
	print(num_blank_address, 'incident(s) had an address of "BLANK".')

def convert_to_csv(data_path, incidents):
	csv_rows = [['Date', 'Dispatch Time', 'Address', 'Quadrant', 'Response Time', 'Unit']]
	errors = []
	addresses = defaultdict(int)

	i = 0
	for index, incident in incidents.iterrows():
		i += 1
		date = incident['Date'].date()
		time = incident['Dispatch Time (HH:MM:SS)']
		address = incident['Location']
		if (not isinstance(address, str)):
			errors.append(('no address', incident))
			continue
		address = normalize_address(address)
		if (address == "BLANK"):
			errors.append(('blank address', incident))
			continue
		addresses[address] += 1
		quadrant = address_quadrant(address)
		response_time = incident['Response Time (HH:MM:SS)']
		unit = incident['Unit']
		csv_rows.append([date, time, address, quadrant, response_time, unit])

	csv_path = data_path + '/dc-emergency-response-data.csv'
	addresses_path = data_path + '/addresses.csv'
	with open(csv_path, 'w') as csv_file:
		writer = csv.writer(csv_file)
		for row in csv_rows:
			writer.writerow(row)
	sorted_addresses = OrderedDict(sorted(addresses.items(), key=lambda t: t[0]))
	with open(addresses_path, 'w') as addresses_file:
		writer = csv.writer(addresses_file)
		for address, count in sorted_addresses.items():
			writer.writerow([address])

	if (len(errors) > 0):
		print_summary(len(csv_rows) - 1, errors)

def import_incident(row):
	incident = []
	for col in row:
		incident.append(col.value)
	return incident

def import_erda_file(file_name):
	'''Imports an Excel file with the specified name.'''
	print(file_name)
	xl_file = pd.ExcelFile(file_name)
	data_frame = xl_file.parse('DATA')
	print(data_frame.shape[0], 'incident(s)')
	return data_frame

def import_erda_files(data_path):
	'''Imports all Excel files in the specified directory.'''
	file_names = glob.glob(data_path + "/*.xlsx")
	data_frames = []
	for file_name in file_names:
		data_frames.append(import_erda_file(file_name))

	incidents = pd.concat(data_frames)
	print(incidents.shape[0], 'incident(s) loaded.')
	convert_to_csv(data_path, incidents)

def usage():
	'''Prints a help string.'''
	print("usage: buildcsv.py <dirname>")

if __name__ == "__main__":
	if (len(sys.argv) == 2):
		import_erda_files(sys.argv[1])
	else:
		usage()
