import requests
import pandas as pd
from funcy import first, second, last, nth
from collections import namedtuple

STREET_TYPES = {
    'AVE': 'AVENUE',
    'DR': 'DRIVE',
    'ST': 'STREET'
}

GRANDMASTER_ADDRESS_URL = 'http://grandmaster-dc.herokuapp.com/api/addresses/search?quadrant=%s&street_type=%s&street=%s'

Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])

def get_geo_codes(address):
    """
        Return co-ordinates of an address by query grandmaster-dc api as tuple
        e.g (latitude =38.889788, longitude=-76.982198)
    """

    street_name = second(address)
    quadrant = last(address)
    street_type = nth(2, address)

    full_street_type = STREET_TYPES.get(street_type, 'STREET')

    url = GRANDMASTER_ADDRESS_URL % (quadrant, full_street_type, street_name)

    adress_data = first(requests.get(url).json())

    if adress_data:
        longitude =  first(adress_data['location']['coordinates'])
        latitude =  second(adress_data['location']['coordinates'])

        return Coordinates(latitude, longitude)

    return Coordinates(latitude=0, longitude=0)

if __name__ == "__main__":
    # Remove .head(10) or change the number to read desired number of rows from CSV file
    try:
        incidents = pd.read_csv('incidents_with_latlongs.csv').head(10)
    except IOError:

        raise Exception("Please Make sure data file \"incidents_with_latlongs.csv\" is present in base directory")

    for idx, incident in incidents.iterrows():
        address = incident['address'].split(' ')

        print get_geo_codes(address)
