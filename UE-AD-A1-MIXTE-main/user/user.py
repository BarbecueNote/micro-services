from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# Appel de gRPC
import grpc
import booking_pb2
import booking_pb2_grpc

# Fonction pour obtenir la liste des réservations
def get_list_bookings(stub):
    allbookings = stub.GetListBookings(booking_pb2.Empty())
    for booking in allbookings:
        print(f"Réservation appelée {booking}")

# Fonction pour obtenir les réservations par ID utilisateur
def get_bookings_by_userid(stub, id):
    bookings = stub.GetBookingsByUserId(booking_pb2.UserId(id=id))
    for booking in bookings:
        print(f"Réservation appelée {booking}")

# Fonction pour effectuer une réservation
def make_reservation(stub, request):

    # Envoyer une requête POST au serveur
    response = stub.AddBooking(request)
    for booking in response:
        print(f"Réservation appelée {booking}")

def run():
    # NOTE (Équipe gRPC Python) : .close() est possible sur un canal et doit être
    # utilisé dans des circonstances où l'instruction with ne convient pas aux besoins
    # du code.
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

# Route pour la page d'accueil
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Bienvenue sur le service utilisateur !</h1>"

# Route pour obtenir la liste des utilisateurs
@app.route("/users", methods=['GET'])
def get_users():
   res = make_response(jsonify(users),200)
   return res

# Route pour obtenir un utilisateur par ID
@app.route("/users/<id>", methods=['GET'])
def get_user_byid(id):
   for user in users:
      if user["id"] == str(id):
         res = make_response(jsonify(user),200)
         return res
   return make_response(jsonify({"error": "mauvais paramètre d'entrée"}), 400)

# Fonction pour sauvegarder les données utilisateur
def save_user_data(users_data):
   users_file_path = "./data/users.json"
   with open(users_file_path, "w") as file:
        json.dump({"users": users_data}, file)
        
# Route pour ajouter un utilisateur
@app.route("/users/<userid>", methods=['POST'])
def add_user(id):
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify({"error": "L'utilisateur existe déjà"}), 409)
    users.append(req)
    save_user_data(users)
    res = make_response(jsonify(req), 200)
    return res

# Route pour obtenir les réservations par ID utilisateur
@app.route("/users/<id>/reservations", methods=['GET'])
def get_reservations_byid(id):
   for user in users:
      if user["id"] == str(id):
         res = make_response(jsonify(requests.get("http://" + request.host.split(':')[0] + ":3201/bookings/"+id).json()),200)
         return res
   return make_response(jsonify({"error": "mauvais paramètre d'entrée"}), 400)

# Route pour obtenir les films réservés par ID utilisateur
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
   return make_response(jsonify({"error": "mauvais paramètre d'entrée"}), 400)

if __name__ == "__main__":
   print("Serveur en cours d'exécution sur le port %s"%(PORT))
   app.run(host=HOST, port=PORT)
