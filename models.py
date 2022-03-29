from locale import normalize
import requests
from flask import render_template, request
import csv, json
from dotenv import dotenv_values
# from datetime import datetime
import time, datetime

config = dotenv_values(".env")
GEO_URL = "https://us1.locationiq.com/v1/search.php"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric"
WEATHER_HIST_URL = "https://history.openweathermap.org/data/3.0/history/timemachine?lat=%s&lon=%s&dt=%s&appid=%s"
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

    def __init__(self):
        self.coordinates = None

    def your_coordinates(self, address):
        
        if self.__validate_address_input(address):
        #Your unique private_token should replace value of the private_token variable.
        #To know how to obtain a unique private_token please refer the README file for this script.

            phys_address = " ".join([i for i in address.values()])

            data = {
                'key': config["LOCATION_TOKEN"],
                'q': phys_address,
                'format': 'json'
            }

            response = requests.get(GEO_URL, params=data)

            latitude = response.json()[0]['lat']
            longitude = response.json()[0]['lon']

            res = {"location": address, "latitude": latitude, "longitude": longitude}
            # self.coordinates = res
            
            return res
            # return render_template("geolocation_result.html", coordinates=res)
        
        else:
            return False
    
    # def read_address_file(self, infile):
    #     res = dict()
    #     with open(infile, "r") as file:
    #         reader = csv.DictReader(file)
    #         address_id = 0
    #         for row in reader:
    #             if self.__validate_address_file(row):
    #                 address = " ".join([row['Street_Address'], row["Street_Name"], row["Zip"], row["Country"]])
    #                 data = {
    #                 'key': config["LOCATION_TOKEN"],
    #                 'q': address,
    #                 'format': 'json'
    #                 }

    #                 response = requests.get(GEO_URL, params=data)
    #                 try:
    #                     latitude = response.json()[0]['lat']
    #                     longitude = response.json()[0]['lon']

    #                     res[address_id] = {"location": address,"latitude": latitude, "longitude": longitude}
                    
    #                 except:
    #                     res[address_id] = {"location": f"ERROR: {address}"}

    #             else:
    #                 res[address_id] = {"location": f"INVALID: {address}"}
                
    #             address_id += 1
        
    #     return res

                
    def __validate_address_input(self, address):
        st_num = address["street_number"].split()
        st_name = address["street_name"].split()
        city = address["city"].split()

        if all([[i.isnumeric() for i in st_num],\
            [i.isalpha() for i in st_name],\
                [i.isalpha() for i in city],\
                    (address["state"] in STATES.keys() or address["state"] in STATES.values()),\
                        self.__valid_zip(address["zip"])]):
                        return True
        else:
            return False
    
    def __validate_address_file(self, address):
        '''
        param: dict object
        '''
        st_num = address["Street_Address"].split()[0]
        if st_num.isnumeric() and self.__valid_zip(address["Zip"]):
            return True


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
    
    def current_location(self):
        curr_location = {
            "street_number": request.form["st_number"],
            "street_name": request.form["st_name"],
            "unit": request.form["unit"],
            "city": request.form["city"],
            "state": request.form["state"],
            "zip": request.form["zip"]
        }

        return curr_location
        

class Weather(FindCoordinates):

    def __init__(self, location_data):
        self.loc_data = location_data
        # self.data_raw = self.weather()
        self.basic = self.__setup_api()

    def weather_forecast(self):

        # data = {
        #     "key": config['WEATHER_TOKEN'],
        #     "lat": self.loc_data['latitude'],
        #     "lon": self.loc_data['longitude'],
        #     "address": self.loc_data['location']
        # }

        data = self.basic

        url = WEATHER_URL % (data['lat'], data['lon'], data['key'])

        response = requests.get(url)

        res = json.loads(response.text)

        offset = res['timezone_offset']

        res = self.normalize_dt(res, offset)

        return res
    
    def normalize_dt(self, data, offset):

        if isinstance(data, str):
            return
        
        if isinstance(data, dict):

            for key in data.keys():
                if (key == 'dt' or key =='sunrise' or key == 'sunset'):
                    data[key] = self.__unix_to_time(data[key], offset)
                else:
                    self.normalize_dt(data[key], offset)
        
        if isinstance(data, list):

            for item in data:
                self.normalize_dt(item, offset)
        
        return data
    
    # def weather_hist(self, start_date):
    '''
    historical data are available only to paid subscribers.
    Function out of order for now.
    '''
    #     api_data = self.basic

    #     start_date = str(int(self.__to_unix(start_date)))

    #     url = WEATHER_HIST_URL % (api_data['lat'], api_data['lon'], start_date, api_data['key'])

    #     response = requests.get(url)

    #     res = json.loads(response.text)

    #     offset = res['timezone_offset']

    #     res = self.normalize_dt(res, offset=0)

    #     return res
    

    def __setup_api(self):
        res = {
            "key": config['WEATHER_TOKEN'],
            "lat": self.loc_data['latitude'],
            "lon": self.loc_data['longitude'],
            "address": self.loc_data['location']
        }

        return res
        
    def __unix_to_time(self, timestamp, offset):
        res = datetime.datetime.utcfromtimestamp(int(timestamp)+int(offset)).strftime('%Y-%m-%d %H:%M:%S')
        return res

    def __to_unix(self, date_time):
        _time = date_time.split()[0].split("-")
        _time = list(map(int, _time))
        date_ = datetime.datetime(_time[0], _time[1], _time[2], 0, 0)
        res = time.mktime(date_.timetuple())
        return res




