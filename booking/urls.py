from audioop import add
from django.urls import path
from .views import add_coach, book_seat, get_all_seats, get_available_seats, get_booked_seats, remove_coach, update_coach

urlpatterns = [
    path('add-coach/', add_coach),
    path('remove-coach/<str:coach_no>/', remove_coach),
    path('update-coach/', update_coach),
    path('get-seats/', get_all_seats),
    path('book-seat/', book_seat),
    path('get-available-seats/', get_available_seats),
    path('get-booked-seats/', get_booked_seats)
]