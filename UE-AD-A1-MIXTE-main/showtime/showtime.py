import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

# Définition du servicer ShowtimeServicer
class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        # Chargement des données de l'horaire à partir du fichier JSON
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
    
    # Méthode pour obtenir les films par heure
    def GetMovieByTime(self, request, context):
        for schedule in self.db:
            if schedule['date'] == request.time:
                for movieid in schedule['movies']:
                    # Renvoie l'ID du film correspondant
                    yield showtime_pb2.MovieID(id=movieid)
            else:
                # Renvoie une chaîne vide si l'heure n'a pas été trouvée
                yield showtime_pb2.MovieID(id='')

    # Méthode pour obtenir l'horaire complet
    def Showtimes(self, request, context):
        for schedule in self.db:
            # Renvoie l'heure et les IDs des films correspondants
            yield showtime_pb2.Schedules(time=schedule["date"], ids=schedule["movies"])

# Fonction pour démarrer le serveur gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()

# Point d'entrée du script
if __name__ == '__main__':
    serve()
