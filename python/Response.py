# User provides a path to the folder containing the original response times
## This script takes the 4 csv files, binds them together, does some basic parsing, and writes to a file. 
## Another file should be used to map latitude and longditude coordinates to street addresses
import sys
import glob
import pandas as pd
import csv

# Parses out the quadrant from the address
def stringToQuadrant(strQuadrant):
	addr = strQuadrant.strip()
	quad = addr.split(" ")
	if "NW" in quad:
		return "NW"
	elif "NE" in quad:
		return "NE"
	elif "SW" in quad:
		return "SW"
	elif "SE" in quad:
		return "SE"
	else:
		return "NA"

def convert_to_csv(data_path, events):
	print('Converting to CSV...')
	print(events.shape)
	csv_rows = [['Date', 'Dispatch Time', 'Address', 'Quadrant', 'Response Time', 'Unit']]

	i = 0
	for index, event in events.iterrows():
		i += 1
		date = event['Date'].date()
		time = event['Dispatch Time (HH:MM:SS)']
		address = event['Location']
		quadrant = ''
		if (not isinstance(address, str)):
			print('Warning: empty address detected:', i, date, time)
			address = ''
		else:
			address = address.strip()
			quadrant = stringToQuadrant(address)
		response_time = event['Response Time (HH:MM:SS)']
		unit = event['Unit']
		csv_rows.append([date, time, address, quadrant, response_time, unit])

	csv_path = data_path + '/dc-emergency-response-data.csv'
	with open(csv_path, 'w') as csv_file:
		writer = csv.writer(csv_file)
		for row in csv_rows:
			writer.writerow(row)

def import_event(row):
	event = []
	for col in row:
		event.append(col.value)
	return event

def import_erda_file(file_name):
	'''Imports an Excel file with the specified name.'''
	print(file_name)
	xl_file = pd.ExcelFile(file_name)
	data_frame = xl_file.parse('DATA')
	print(data_frame.shape)
	return data_frame

def import_erda_files(data_path):
	'''Imports all Excel files in the specified directory.'''
	file_names = glob.glob(data_path + "/*.xlsx")
	data_frames = []
	for file_name in file_names:
		data_frames.append(import_erda_file(file_name))
	convert_to_csv(data_path, pd.concat(data_frames))

def usage():
	'''Prints a help string.'''
	print("usage: Response.py <dirname>")

if __name__ == "__main__":
	if (len(sys.argv) == 2):
		import_erda_files(sys.argv[1])
	else:
		usage()
