import requests
from flask import Flask, render_template, request
from flask import render_template
from models import FindCoordinates as coor

app = Flask(__name__)

SPACE = " "


@app.route("/", methods=["POST", "GET"])
def your_coordinates():
    

    if request.method == "POST":

        # curr_location = str(
        #     request.form["st_number"]+SPACE+
        #     request.form["st_name"]+SPACE+
        #     request.form["unit"]+SPACE+
        #     request.form["city"]+SPACE+
        #     request.form["state"]+SPACE+
        #     request.form["zip"]
        # )
        
        curr_location = {
            "street_number": request.form["st_number"],
            "street_name": request.form["st_name"],
            "unit": request.form["unit"],
            "city": request.form["city"],
            "state": request.form["state"],
            "zip": request.form["zip"]
        }

        return coor().your_coordinates(curr_location)
        
    else:
        return render_template("geolocation.html")
    
    

    


if __name__ == ("__main__"):
    app.run(host='0.0.0.0',port=8000, debug=True)
