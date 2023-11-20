from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

# Chargement des données d'utilisateurs depuis le fichier JSON
with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

# Route pour la page d'accueil
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Bienvenue sur le service utilisateur!</h1>"

# Route pour obtenir la liste des utilisateurs
@app.route("/users", methods=['GET'])
def get_users():
   res = make_response(jsonify(users), 200)
   return res

# Route pour obtenir un utilisateur par son ID
@app.route("/users/<id>", methods=['GET'])
def get_user_byid(id):
   for user in users:
      if user["id"] == str(id):
         res = make_response(jsonify(user), 200)
         return res
   return make_response(jsonify({"error": "mauvais paramètre d'entrée"}), 400)

# Route pour obtenir les réservations d'un utilisateur par son ID
@app.route('/users/<id>/reservations', methods=['GET'])
def get_reservations_byid(id):
    """This function gets the user's reservations by their ID."""
    # Search for the user with the provided 'id'.
    for user in users:
        if user["id"] == id:
            # Make a request to the booking service to get reservations for the user.
            response = requests.get(f"http://{request.host.split(':')[0]}:3201/bookings/{id}")
            if response.status_code == 200:
                # If reservations are found, merge user and reservation data.
                merged_dict = {**user, "reservations": response.json()}
                return make_response(jsonify(merged_dict), 200)
            else:
                # If no reservations are found, return an error response.
                return make_response(jsonify({"error": "Booking information not found"}), 400)

    # If the user with the provided 'id' is not found, return an error response.
    return make_response(jsonify({"error": "User not found"}), 400)


# Route pour obtenir les films réservés par un utilisateur par son ID
@app.route("/users/<id>/reservations/movies", methods=['GET'])
def get_reservations_movies_byid(id):
   for user in users:
      if user["id"] == str(id):
         reservations = requests.get("http://" + request.host.split(':')[0] + ":3201/bookings/"+id).json()
         films = []
         for date in reservations["dates"]:
            for movies in date['movies']:
               movie = requests.get("http://" + request.host.split(':')[0] + ":3200/movies/"+movies).json()
               films.append(movie)
         res = make_response(jsonify(films), 200)
         return res
   return make_response(jsonify({"error": "mauvais paramètre d'entrée"}), 400)

# Point d'entrée du script
if __name__ == "__main__":
   print("Serveur en cours d'exécution sur le port %s"%(PORT))
   app.run(host=HOST, port=PORT)
