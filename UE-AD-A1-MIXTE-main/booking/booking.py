import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import json

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetListBookings(self, request, context):
        for booking in self.db:
            for date in booking['dates']:
                yield booking_pb2.BookingData(userId=booking['userid'], dates=date['date'], moviesId=date['movies'])


    def GetBookingsByUserId(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.id:
                for user in booking['dates']:
                    yield booking_pb2.BookingData(userId= booking['userid'], dates=user['date'], moviesId=user['movies'])

        return booking_pb2.BookingData(userId ="" , dates="", moviesId="")

    def AddBooking(self, request, context):
        created=False
        movie = request.movie
        for booking in self.db:
            if booking['userid'] == request.id:
                for date in booking['dates']:
                    if date['date'] == request.date:
                        created=True
                        date['movies'].append(movie)
                    yield booking_pb2.BookingData(userId =booking['userid'] , dates=date['date'], moviesId=date['movies'])

                if created==False:

                    addedbooking = {
                                    "date": request.date,
                                    "movies": [movie]
                                    }
                    booking['dates'].append(addedbooking)
                    created = True
                    for date in booking['dates']:
                        yield booking_pb2.BookingData(userId=booking['userid'], dates=date['date'],
                                                      moviesId=date['movies'])
        if created==False:
            addedbooking = {
                            "userid": request.id,
                            "dates": [
                                        {
                                            "date": request.date,
                                            "movies": [movie]
                                        }
                                    ]
                            }
            booking.append(addedbooking)
            return booking_pb2.BookingData(addedbooking)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()

def get_movie_by_time(stub,time):
    movies = stub.GetMovieByTime(showtime_pb2.Timestamp(time=time))
    for movie in movies:
        print(movie)

def showtimes(stub):
    movies = stub.Showtimes(showtime_pb2.Empty())
    for movie in movies:
        print(movie)

def run():
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetMovieByTime --------------")
        time = "20151201"
        get_movie_by_time(stub, time)
        print ("*******************************************")
        showtimes(stub)


if __name__ == '__main__':
    #serve()
    run()
