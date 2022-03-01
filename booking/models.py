from django.conf import settings
from django.db import models

class Seat (models.Model):
    seat_no = models.CharField(primary_key=True, max_length=10)
    is_booked = models.BooleanField(default=False)
    coach = models.ForeignKey("Coach", related_name='seats', on_delete=models.CASCADE)

class Coach (models.Model):
    coach_no = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)

class Booking (models.Model):
    booking_id = models.CharField(primary_key=True, max_length=10)
    seat = models.ForeignKey("Seat", on_delete=models.CASCADE)
    coach = models.ForeignKey("Coach", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)