from flask import Flask, render_template, request
# from flask import render_template
from models import FindCoordinates as coor
from models import Weather
import os

app = Flask(__name__)

SPACE = " "

PWD = os.getcwd()+"/"


@app.route("/", methods=["POST", "GET"])
def your_coordinates():
    

    if request.method == "POST":
        curr_location = coor().current_location()

        res = coor().your_coordinates(curr_location)
        if res:
            return render_template("geolocation_result.html", coordinates=res)
        else:
            return render_template("geolocation.html", message="Invalid Address")
        
    else:
        return render_template("geolocation.html")
    

@app.route("/address_file", methods=["POST", "GET"])
def process_addresses():

    if request.method == "POST":
        infile = request.form["input_file"]
        infile = PWD+infile
        res = coor().read_address_file(infile)
        return render_template("geolocation_file_result.html", locations=res)
    
    else:
        return render_template("geolocation_file.html")

@app.route("/coordinates&weather", methods=["POST", "GET"])
def coordinates_and_weather():

    if request.method == "POST":
        curr_location = coor().current_location()

        loc_data = coor().your_coordinates(curr_location)

        data = Weather(loc_data).weather_forecast()

        return render_template("coordinates&weather_result.html", data=data)
        
    else:
        return render_template("geolocation&weather.html")

@app.route("/weather-history", methods=["POST", "GET"])
def weather_history():
    if request.method == "POST":
        curr_location = coor().current_location()

        loc_data = coor().your_coordinates(curr_location)

        start_date = request.form["start_date"]

        data = Weather(loc_data).weather_hist(start_date)

        return render_template("weather_history_result.html", test=data)

        

    else:
        return render_template("weather_history.html")

    
if __name__ == ("__main__"):
    app.run(host='0.0.0.0',port=8000, debug=True)
