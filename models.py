import requests
from flask import render_template


URL = "https://us1.locationiq.com/v1/search.php"


class FindCoordinates:

    # def your_address():
    #     address = input("Input the address: ")
    #     return address

    def your_coordinates(address):

        # address = input("Input the address: ")

        #Your unique private_token should replace value of the private_token variable.
        #To know how to obtain a unique private_token please refer the README file for this script.
        private_token = "pk.bad269d9e06d0b3e9d42ff3dcba0bba0"

        data = {
            'key': private_token,
            'q': address,
            'format': 'json'
        }

        response = requests.get(URL, params=data)


        latitude = response.json()[0]['lat']
        longitude = response.json()[0]['lon']

        res = {"location": address, "latitude": latitude, "longitude": longitude}

        return render_template("geolocation_result.html", coordinates=res)