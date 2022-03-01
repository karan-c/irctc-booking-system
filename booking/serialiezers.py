from dataclasses import field, fields
from rest_framework import serializers
from .models import Seat, Coach, Booking

class SeatSearializer(serializers.ModelSerializer):
    coach_type = serializers.SerializerMethodField(read_only=True)
    coach_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Seat
        fields = ['seat_no', 'is_booked', 'coach_type', 'coach_id']

    def get_coach_type(self, obj):
        return obj.coach.type

    def get_coach_id(self, obj):
        return obj.coach.coach_no
