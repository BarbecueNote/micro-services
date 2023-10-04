from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
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
