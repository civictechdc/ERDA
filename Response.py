import csv

def stringToDate(strDate):
	secs = 0
	if strDate:
		time = strDate.split(":")
		secs = (int(time[0]) * 3600) + (int(time[1]) * 60) + int(time[2])
	return secs

def translateVehicleType(strVehicle):
	if vehicle == "MED" or vehicle == "AMB" or vehicle == "EMS SUP":
		return "Medical"
	elif vehicle == "ENG" or vehicle == "TRUCK":
		 return "Fire"
	elif vehicle == "OTH":
		return "Other"
	else:
		return strVehicle

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
	# Open and read file
	data = open('fullEmergencyData.csv', "r")
	emer = csv.DictReader(data)

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
		
		response_time.append(stringToDate(time))

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
