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