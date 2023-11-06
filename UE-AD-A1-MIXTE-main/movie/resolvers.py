import json

from graphql import GraphQLError

# Fonction pour obtenir un film par son ID
def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie
        raise GraphQLError("mauvais paramètre d'entrée")

# Fonction pour obtenir un film par son titre
def movie_with_title(_, info, _title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie
        raise GraphQLError("mauvais paramètre d'entrée")

# Fonction pour mettre à jour la note d'un film
def update_movie_rate(_, info, _id, _rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile, indent=4)
    return newmovie

# Fonction pour mettre à jour le titre d'un film
def update_movie_title(_, info, _id, _title):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['title'] = _title
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile, indent=4)
    return newmovie

# Fonction pour créer un nouveau film
def create_movie(_, info, _movie):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _movie['id']:
                raise GraphQLError("un élément existant existe déjà")
        newmovie = _movie
        newmovies = movies
        newmovies["movies"].append(newmovie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile, indent=4)
    return newmovie

# Fonction pour supprimer un film par son ID
def delete_movie(_, info, _id):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        newmovies = movies
        for movie in movies['movies']:
            if movie['id'] == _id:
                newmovie = movie
                newmovies["movies"].remove(newmovie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile, indent=4)
    return newmovie

# Fonction pour obtenir les acteurs dans un film
def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors
