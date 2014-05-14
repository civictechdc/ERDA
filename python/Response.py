# User provides a path to the folder containing the original response times
## This script takes the 4 csv files, binds them together, does some basic parsing, and writes to a file. 
## Another file should be used to map latitude and longditude coordinates to street addresses
from os import listdir
from os.path import isfile, join	
import csv
import pandas as pd
import glob

# Takes in a string time value in HH:MM:SS format, outputting an integer seconds
def timeToSeconds(strDate):
	secs = 0
	if strDate:
		time = strDate.split(":")
		secs = (int(time[0]) * 3600) + (int(time[1]) * 60) + int(time[2])
	return secs
# sorts the response vehicle types into Medical, Fire, or Other
def translateVehicleType(strVehicle):
	if vehicle == "MED" or vehicle == "AMB" or vehicle == "EMS SUP":
		return "Medical"
	elif vehicle == "ENG" or vehicle == "TRUCK":
		 return "Fire"
	elif vehicle == "OTH":
		return "Other"
	else:
		return strVehicle
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

if __name__ == "__main__":

	mypath = raw_input('What is the path to the ERDA data? \n ')

	# Get all files in the specified directory
	erdafiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

	print(erdafiles)

	e1 = open(erdafiles[0], "r")
	e2 = open(erdafiles[1], "r")
	allFiles = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()
    list = []
    for files in allFiles:
        df = pd.read_csv(join(directory,files),index_col=None, header=0)
        list.append(df)
    frame = pd.concat(list)

	# Open and read file
	#	data = open('fullEmergencyData.csv', "r")
	#	emer = csv.DictReader(data)

	# Final Columns
	response_time = []
	vehicle_type = []
	city_quadrant = []
	time_of_day = []
	month = []
	holiday = []

	# Response Time
	for row in emer:
		time = row['Response.Time..HH.MM.SS.']
		
		response_time.append(stringToSeconds(time))
		
	# Vehicle Type
		vehicle = row['Unit']
		vehicle_type.append(translateVehicleType(vehicle))
			
	# City Quadrant
		address = row['Location']
		city_quadrant.append(stringToQuadrant(address))
		
	# Time of Day
		hr = int((row['Dispatch.Time..HH.MM.SS.'].split(":"))[0])
		time_of_day.append(hr)

	# Month
		mon = int((row['Date'].split("/"))[0])
		month.append(mon)

	# Write to CSV
	rows = zip(response_time, vehicle_type, city_quadrant, time_of_day, month)

	with open('test.csv', 'w') as f:
		writer = csv.writer(f)
		for row in rows:
			writer.writerow(row)

