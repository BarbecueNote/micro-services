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
                yield booking_pb2.BookingData(userId=booking['userid'], dates=date['date'],
                                              moviesId=date['movies'])


    def GetBookingsByUserId(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.id:
                for user in booking['dates']:
                    yield booking_pb2.BookingData(userId= booking['userid'],
                                                  dates=user['date'], moviesId=user['movies'])

        return booking_pb2.BookingData(userId ="" , dates="", moviesId="")

    def AddBooking(self, request, context):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            db = json.load(jsf)
        created=False
        rmovie = list(request.moviesId)
        for booking in db['bookings']:
            if booking['userid'] == request.userId:
                for date in booking['dates']:
                    for movie in date['movies']:
                        if [movie] == rmovie:
                            created = True
                            print("booking already exists")
                    if date['date'] == request.dates and created==False:
                        created=True
                        date['movies'] = date['movies'] + rmovie
                        with open("{}/data/bookings.json".format("."), "w") as json_file:
                            json.dump(db, json_file, indent=3)

                if created==False:
                    addedbooking = {"date": request.dates,
                                    "movies": rmovie
                                    }
                    booking['dates'].append(addedbooking)
                    newcontent = db
                    with open("{}/data/bookings.json".format("."), "w") as json_file:
                        json.dump(newcontent, json_file, indent=3)
                    print(booking['dates'])
                    created = True

        if created==False:
            addedbooking = {
                            "userid": request.userId,
                            "dates": [
                                        {
                                            "date": request.dates,
                                            "movies": rmovie
                                        }
                                    ]
                            }
            db['bookings'].append(addedbooking)
            with open("{}/data/bookings.json".format("."), "w") as json_file:
                json.dump(db, json_file, indent=3)
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            update = json.load(jsf)["bookings"]
        for booking in update:
            if booking['userid'] == request.userId:
                for user in booking['dates']:
                    yield booking_pb2.BookingData(userId=booking['userid'], dates=user['date'],
                                                  moviesId=user['movies'])

        return booking_pb2.BookingData(userId="", dates="", moviesId="")


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
    movies = stub.Showtimes(showtime_pb2.EmptyMessage())
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
    serve()
    run()
