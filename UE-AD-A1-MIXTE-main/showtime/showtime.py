import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
    
    def GetMovieByTime(self,request,context):
        for schedule in self.db:
            if schedule['date'] == request.time:
                for movieid in schedule['movies']:
                    yield showtime_pb2.MovieID(id=movieid)
            else:
                yield showtime_pb2.MovieID(id='')

    def Showtimes(self, request, context):
        for schedule in self.db:
            yield showtime_pb2.Schedules(time=schedule["date"], ids=schedule["movies"])

'''    def Showtimes(self, request, context):
        for schedules in self.db:
            for schedule in schedules['date']:
                    """HERE 'schedule[movies]' is a list of string 
                    f you decide to build a lst of MovieID instead you must create it"""
                    my_movie_ids = []
                    # TODO build a list of MovieID 
                    for id in schedule[]:
                        pass #TODO add a MovieId to my_movie_ids
                yield showtime_pb2.Schedules(time=schedule, ids=schedule["movies"])'''


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
