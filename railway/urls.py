from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    AddTrainView,
    SeatAvailabilityView,
    BookSeatView,
    BookingDetailView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/add_train/', AddTrainView.as_view(), name='add_train'),
    path('trains/', SeatAvailabilityView.as_view(), name='seat_availability'),
    path('bookings/', BookSeatView.as_view(), name='book_seat'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
]
