import requests
from flask import Flask, render_template, request
from flask import render_template
from models import FindCoordinates as coor

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def your_coordinates():

    if request.method == "POST":

        curr_location = str(request.form["curr_location"]).strip(" ")

        return coor.your_coordinates(curr_location)
        # return display_result(curr_location)
        
    else:
        return render_template("geolocation.html")

# @app.route("/coordinates")
# def display_result(location):
#     return coor.your_coordinates(location)


        
    


        

    
    

    # address = input("Input the address: ")

    # #Your unique private_token should replace value of the private_token variable.
    # #To know how to obtain a unique private_token please refer the README file for this script.
    # private_token = "pk.bad269d9e06d0b3e9d42ff3dcba0bba0"

    # data = {
    #     'key': private_token,
    #     'q': address,
    #     'format': 'json'
    # }

    # response = requests.get(url, params=data)


    # latitude = response.json()[0]['lat']
    # longitude = response.json()[0]['lon']
    
    

    


if __name__ == ("__main__"):
    app.run(host='0.0.0.0',port=8000, debug=True)
