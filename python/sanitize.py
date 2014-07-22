import re

def categorize_rows(data):
    '''Returns a list of tuples, (data_header, data_type)'''
    first_row = data[0] if a else None
    data_headers = None
    result = None
    if first_row:
        result = []
        data_headers = first_row.keys()
        for row in data:
            #check for all types.
            for header in data_headers:
                if match_date(row[header]):
                    result.append((header, "Date"))
                elif match_time(row[header]):
                    result.append((header, "Time"))
                elif match_unit(row[header]):
                    result.append((header, "Unit"))
                elif match_location(row[header]):
                    result.append((header, "Location"))
                else:
                    result.append((header, None))
    return result           

def sanitize_data(data):
    '''Takes in the data and attempts to sanitize it. Returns a tuple of all matched and all failed rows.'''
    #For the future, should we attempt to automatically detect what we are parsing instead of depending on hard-coded header names?
    matchList = []
    errorList = []
    headers_categorized = categorize_data(data)
    for row in data:
        failure = []
        if not match_date(row["Date"]):
            failure.append(row["Date"])
            
        if not match_time(row["Time"]):
            failure.append(row["Time"])
            
        if not match_unit(row["Unit"]):
            failure.append(row["Unit"])
            
        if not match_location(row["Location"]):
            failure.append(row["Location"])
        
        if not failure:
            matchList = row
        else:
            errorList = row #FIXME maybe append the errors?
            
    return (matchList, errorList)

dateRegex = re.compile("\\d\\d/\\d\\d/\\d\\d\\d\\d")
timeRegex = re.compile("\\d\\d:\\d\\d:\\d\\d")
unitRegex = re.compile("ENG|TRUCK|AMB|MED|EMS SUP|OTH")
locationRegex = re.compile(".+")

def match_date(string):
    return dateRegex.match(string)

def match_time(string):
    return timeRegex.match(string)

def match_unit(string):
    return unitRegex.match(string)

def match_location(string):
    return locationRegex.match(string)
