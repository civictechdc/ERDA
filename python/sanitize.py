import re

def categorize_rows(data):
    '''Accepts something equivalent to a csv.DictReader object. Returns a map of header name to type.'''
    result = {}
    for row in data:
        #check for all types.
        for entry in row.keys():
            result[entry] = []
            if match_date(row[entry]):
                result[entry].append("Date")
            if match_time(row[entry]):
                result[entry].append("Time")
            if match_unit(row[entry]):
                result[entry].append("Unit")
            if not result[entry] and match_other(row[entry]):
                result[entry].append("Other")
    return result

dateRegex = [re.compile("\\d\\d/\\d\\d/\\d\\d\\d\\d"), re.compile("\\d\\d-\\d\\d-\\d\\d\\d\\d"), re.compile("\\d\\d\\d\\d/\\d\\d/\\d\\d"), re.compile("\\d\\d\\d\\d-\\d\\d-\\d\\d")]
timeRegex = re.compile("\\d\\d:\\d\\d:\\d\\d")
unitRegex = re.compile("ENG|TRUCK|AMB|MED|EMS SUP|OTH")
otherRegex = re.compile(".+")

def match_date(string):
    result = []
    for regex in dateRegex:
        if regex.search(string):            
            result.append(regex.search(string))
    return result

def match_time(string):
    return timeRegex.search(string)

def match_unit(string):
    return unitRegex.search(string)

def match_other(string):
    return otherRegex.search(string)
