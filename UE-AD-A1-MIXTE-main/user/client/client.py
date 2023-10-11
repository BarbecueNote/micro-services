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



    # Créez une demande de réservation
    request = booking_pb2.ReservationRequest(
        customer_name="John Doe",
        room_type="Suite",
        num_guests=2
    )

    # Envoyez la requête POST au serveur
    response = client.MakeReservation(request)

    # Traitez la réponse
    print("Confirmation Number:", response.confirmation_number)
    print("Message:", response.message)

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        client = booking_pb2_grpc.BookingServiceStub(channel)


        print("-------------- GetListBookings --------------")
        #get_list_bookings(stub)
        print("-------------- GetBookingsByUserId --------------")
        userid="garret_heaton"
        get_bookings_by_userid(stub, userid)

    channel.close()


if __name__ == '__main__':
    run()