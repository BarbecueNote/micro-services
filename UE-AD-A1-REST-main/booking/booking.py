from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):

    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            return make_response(jsonify(booking), 200)
    return make_response(jsonify({"error":"bad input parameter"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    req = request.get_json()
    times = requests.get("http://" + request.host.split(':')[0] + ":3202/showtimes").json()
    valid_date = False
    for time in times:
        if str(time["date"]) == str(req["date"]):
            valid_date = True
            #on vérifie si le film existe
            if not all(item in time["movies"] for item in req["movies"]):
                return make_response(jsonify({"error": "bad input parameter"}), 400)
    if not valid_date:
        return make_response(jsonify({"error": "bad input parameter"}), 400)
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            for date in booking["dates"]:
                if str(req["date"]) == str(date["date"]):
                    for movie in date["movies"]:
                        if movie in req["movies"]:
                            return make_response(jsonify({"error": "an existing item already exists"}), 409)
                    date["movies"] += req["movies"]
                    return make_response(jsonify({"message": "Booking created"}), 200)
            booking["dates"].append(req)
            return make_response(jsonify({"message":"Booking created"}), 200)
    return make_response(jsonify({"error": "bad input parameter"}), 400)



if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
