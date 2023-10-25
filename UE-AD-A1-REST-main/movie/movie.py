from flask import Flask, render_template, request, jsonify, make_response
import json
import requests
from urllib.parse import quote

import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), "r") as jsf:
   movies = json.load(jsf)["movies"]


#TMDB API not IMDB
API_KEY = '1f1144d7bdc5b16a570873719d398fee'
   
# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)


@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    URL = f"https://api.themoviedb.org/3/movie/{movieid}?api_key={API_KEY}"
    response = requests.get(URL)
    if response.status_code != 200:
        return make_response(jsonify({"error": "Movie not found"}), 404)
    movie = response.json()
    return make_response(jsonify(movie),200)

@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"bad input parameter"}),400)

    movies.append(req)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res


@app.route("/moviebytitle", methods=['GET'])
def get_movie_bytitle():
    title = request.args.get("title")
    if not title:
        return make_response(jsonify({"error": "Title parameter is required"}), 400)
    encoded_title = quote(title)
    for movie in movies:
        if movie["title"].lower() == title.lower():
            return make_response(jsonify(movie), 200)

    # check tmdb if info doesn't exist locally (IMDB's free plan is off since June) 
    URL = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={encoded_title}"
    response = requests.get(URL)
    search_results = response.json().get("results", [])

    if search_results:
        return make_response(jsonify(search_results[0]), 200)
    else:
        return make_response(jsonify({"error": "Movie not found"}), 404)


@app.route("/movies/<movieid>/modifyrate/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route("/movies/<movieid>/modifytitle/<title>", methods=['PUT'])
def update_movie_title(movieid, title):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["title"] = str(title)
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT, debug= True)
