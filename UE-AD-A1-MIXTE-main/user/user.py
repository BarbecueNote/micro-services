# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
import grpc
import booking_pb2
import booking_pb2_grpc

def get_list_bookings(stub):
    allbookings = stub.GetListBookings(booking_pb2.Empty())
    for booking in allbookings:
        print(f"booking called {booking}")

def get_bookings_by_userid(stub, id):
    bookings = stub.GetBookingsByUserId(booking_pb2.UserId(id=id))
    for booking in bookings:
        print(f"booking called {booking}")

def make_reservation(stub, request):

    # Envoyez la requête POST au serveur
    response = stub.AddBooking(request)
    for booking in response:
        print(f"booking called {booking}")

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        print("-------------- GetListBookings --------------")
        #get_list_bookings(stub)
        print("-------------- GetBookingsByUserId --------------")
        #userid="garret_heaton"
        #get_bookings_by_userid(stub, userid)
        print("-------------- AddBooking --------------")
        """request = booking_pb2.BookingData(
            userId="chris_rivers",
            moviesId=["7daf7208-be4d-4944-a3ae-c1c2f516f3e6"],
            dates="20151201"
        )"""
        request = booking_pb2.BookingData(
            userId="jim_halpert",
            moviesId=["7daf7208-be4d-4944-a3ae-c1c2f516f3e6"],
            dates="20151201"
        )
        make_reservation(stub, request)
    channel.close()

if __name__ == '__main__':
    run()


app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_users():
   res = make_response(jsonify(users),200)
   return res

@app.route("/users/<id>", methods=['GET'])
def get_user_byid(id):
   for user in users:
      if user["id"] == str(id):
         res = make_response(jsonify(user),200)
         return res
   return make_response(jsonify({"error": "bad input parameter"}), 400)

@app.route("/users/<userid>", methods=['POST'])
def add_user(id):
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify({"error": "User already exists"}), 409)
    users.append(req)
    res = make_response(jsonify(req), 200)
    return res

@app.route("/users/<id>/reservations", methods=['GET'])
def get_reservations_byid(id):
   for user in users:
      if user["id"] == str(id):
         res = make_response(jsonify(requests.get("http://" + request.host.split(':')[0] + ":3201/bookings/"+id).json()),200)
         return res
   return make_response(jsonify({"error": "bad input parameter"}), 400)
@app.route("/users/<id>/reservations/movies", methods=['GET'])
def get_reservations_movies_byid(id):
   for user in users:
      if user["id"] == str(id):
         reservations = requests.get("http://" + request.host.split(':')[0] + ":3201/bookings/"+id).json()
         films= []
         for date in reservations["dates"]:
            for movies in date['movies']:
               movie = requests.get("http://" + request.host.split(':')[0] + ":3200/movies/"+movies).json()
               films.append(movie)
         res = make_response(jsonify(films),200)
         return res
   return make_response(jsonify({"error": "bad input parameter"}), 400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)