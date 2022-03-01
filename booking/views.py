from calendar import SATURDAY
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Coach, Seat, Booking
from .serialiezers import SeatSearializer


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_coach(Request, *args, **kwargs):
    req_data = Request.data
    if req_data.get('type') != 'seater' and req_data.get('type') != 'ac_sleeper' and req_data.get('type') != 'nonac_sleeper':
        return Response({"message": "Coach type is invalid"}, status=status.HTTP_400_BAD_REQUEST)

    new_coach = Coach.objects.create(type = req_data.get('type'))
    new_coach.save()
    seat_limit = 120 if (req_data.get('type') == 'seater') else 60
    for i in range(seat_limit):
        id = f'{new_coach.coach_no}_{i}'
        seat = Seat.objects.create(seat_no=id, coach=new_coach)
        seat.save()
    return Response({"message": "Coach created successfullly", "coach_no": new_coach.coach_no}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def remove_coach(Request, coach_no, *args, **kwargs):
    coach_obj = Coach.objects.filter(coach_no=coach_no)
    if not coach_obj.exists():
        return Response({"message": "Invalid Coach Number"}, status=status.HTTP_400_BAD_REQUEST)
    coach_obj = coach_obj.first()
    coach_obj.delete()
    return Response({ "message": "Coach Removed Successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_coach(Request, *args, **kwargs):
    req_data = Request.data
    coach_no = req_data.get('coach_no')
    coach_obj = Coach.objects.filter(coach_no=coach_no)

    if not coach_obj.exists():
        return Response({"message": "Invalid Coach Number"}, status=status.HTTP_400_BAD_REQUEST)

    if req_data.get('type') != 'seater' and req_data.get('type') != 'ac_sleeper' and req_data.get('type') != 'nonac_sleeper':
        return Response({"message": "Coach type is invalid"}, status=status.HTTP_400_BAD_REQUEST)
   
    coach_obj = coach_obj.first()
    if 'type' in req_data and coach_obj.type != req_data.get('type'):
        if (coach_obj.type == 'ac_sleeper' or coach_obj.type == 'nonac_sleeper') and req_data.get('type') == 'seater':  # If update is sleeper -> seater then we need to add 60 seats 
            for i in range(60):
                id = f'{coach_no}_{i + 60}'
                seat = Seat.objects.create(seat_no=id, coach=coach_obj)
                seat.save()
        elif coach_obj.type == 'seater': # If update is seater -> sleeper than we need to remove last 60 seats
            for i in range(60):
                id = f'{coach_no}_{i + 60}'
                seat_obj = Seat.objects.get(seat_no = id)
                seat_obj.delete() 
        coach_obj.type = req_data.get('type')
    coach_obj.save()
    return Response({"message": "Coach Details updated successfully"}, status=status.HTTP_200_OK)   
    
@api_view(['GET'])
def get_all_seats(Request, *args, **kwargs):
    seats = Seat.objects.all()
    serializer = SeatSearializer(seats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_seat(Request, *args, **kwargs):
    req_data = Request.data
    seat_details =  req_data.get('seat_details')
    for detail in seat_details:
        seat_no = detail.get('seat_no')
        coach_no = detail.get('coach_no')
        seat_obj = Seat.objects.filter(seat_no = seat_no)
        if not seat_obj.exists():
            return Response({"message": "Seat number is invalid", "seat_no": seat_no}, status=status.HTTP_404_NOT_FOUND)
        coach_obj = Coach.objects.filter(coach_no = coach_no)
        if not coach_obj.exists():
            return Response({"message": "Coach number is invalid", "coach_no": coach_no}, status=status.HTTP_404_NOT_FOUND)
        seat_obj = seat_obj.first()
        if seat_obj.is_booked:
            return Response({"message": "This seat is already booked", "seat_no": seat_no}, status=status.HTTP_400_BAD_REQUEST)

    for detail in seat_details:
        seat_no = detail.get('seat_no')
        coach_no = detail.get('coach_no')
        seat_obj = Seat.objects.filter(seat_no=seat_no)
        seat_obj = seat_obj.first()
        coach_obj = Coach.objects.filter(coach_no=coach_no)
        coach_obj = coach_obj.first()
        booking_id = f'{seat_no}_{Request.user}'
        book_obj = Booking.objects.create(booking_id = booking_id, seat = seat_obj, coach = coach_obj, user = Request.user)
        seat_obj.is_booked = True
        seat_obj.save()
        book_obj.save()
    
    return Response({"message": "Booking succesfull"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_available_seats(Request, *args, **kwargs):
    seats = Seat.objects.filter(is_booked=False)
    serializer = SeatSearializer(seats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_booked_seats(Request, *args, **kwargs):
    seats = Seat.objects.filter(is_booked=True)
    serializer = SeatSearializer(seats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)