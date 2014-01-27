import csv

# Open and read file
data = open('fullEmergencyData.csv', "r")
emer = csv.reader(data)
emer.next()

# Final Columns
response_time = []
vehicle_type = []
city_quadrant = []
time_of_day = []
month = []
holiday = []

# Response Time
for row in emer:
    time = row[4]
    time = time.split(":")

    if time[0] == '00':
        secs = (int(time[0]) * 3600) + (int(time[1]) * 60) + int(time[2])
        response_time.append(secs)
    else:
        response_time.append("NA")

# Vehicle Type
    vehicle = row[5]
    if vehicle == "MED" or vehicle == "AMB" or vehicle == "EMS SUP":
        vehicle_type.append("Medical")
    elif vehicle == "ENG" or vehicle == "TRUCK":
        vehicle_type.append("Fire")
    elif vehicle == "OTH":
        vehicle_type.append("Other")
    else:
        vehicle_type.append("NA")
        
# City Quadrant
    address = row[3]
    addr = row[3].strip()
    if addr[len(addr) - 2 : len(addr)] == "NW":
        city_quadrant.append("NW")
    elif addr[len(addr) - 2 : len(addr)] == "NE":
        city_quadrant.append("NE")
    elif addr[len(addr) - 2 : len(addr)] == "SW":
        city_quadrant.append("SW")
    elif addr[len(addr) - 2 : len(addr)] == "SE":
        city_quadrant.append("SE")
    else:
        quad = addr.split(" ")
        if "NW" in quad:
            city_quadrant.append("NW")
        elif "NE" in quad:
            city_quadrant.append("NE")
        elif "SW" in quad:
            city_quadrant.append("SW")
        elif "SE" in quad:
            city_quadrant.append("SE")
        else:
            city_quadrant.append("NA")

# Time of Day
    hr = int((row[2].split(":"))[0])
    time_of_day.append(hr)

# Month
    mon = int((row[1].split("/"))[0])
    month.append(mon)

# Write to CSV
rows = zip(response_time, vehicle_type, city_quadrant, time_of_day, month)

with open('test.csv', 'wb') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(rows)


