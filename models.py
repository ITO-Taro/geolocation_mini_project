from importlib.util import resolve_name
import requests
from flask import render_template
from pygeocoder import Geocoder


TOKEN = "pk.bad269d9e06d0b3e9d42ff3dcba0bba0"
URL = "https://us1.locationiq.com/v1/search.php"
STATES = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


class FindCoordinates:

    # def your_address():
    #     address = input("Input the address: ")
    #     return address

    def your_coordinates(self, address):
        
        if self.__validate_address(address):
        #Your unique private_token should replace value of the private_token variable.
        #To know how to obtain a unique private_token please refer the README file for this script.
       
            data = {
                'key': TOKEN,
                'q': address,
                'format': 'json'
            }

            response = requests.get(URL, params=data)


            latitude = response.json()[0]['lat']
            longitude = response.json()[0]['lon']

            res = {"location": address, "latitude": latitude, "longitude": longitude}

            return render_template("geolocation_result.html", coordinates=res)
        
        else:
            return render_template("geolocation.html", message="Invalid Address")
    
    def __validate_address(self, address):
        if all([address["street_number"].isnumeric(),\
            address["street_name"].isalpha(),\
                address["city"].isalpha(),\
                    (address["state"] in STATES.keys() or address["state"] in STATES.values()),\
                        self.__valid_zip(address["zip"])]):
                        return True
        else:
            return False
    
    def __valid_zip(self, zip):
        res = None
        if len(zip) < 5:
            res = False
        else:
            if len(zip) == 5 and zip.isnumeric():
                res = True
            else:
                if len(zip) > 5 and '-' in zip:
                    zip = zip.split('-')
                    if all([len(zip[0]) == 5, zip[0].isnumeric(), zip[1].isnumeric()]):
                        res = True
                    else:
                        res = False
                else:
                    res = False
        return res
        
            

