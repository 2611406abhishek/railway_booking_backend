from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from django.conf import settings
from .serializers import RegisterSerializer, LoginSerializer, TrainSerializer, BookingSerializer
from .models import Train, Booking
from rest_framework.authtoken.models import Token

class AdminAPIKeyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY')
        return api_key == settings.ADMIN_API_KEY

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TrainAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated, AdminAPIKeyPermission]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(available_seats=serializer.validated_data.get('total_seats'))
            return Response({"message": "Train added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        trains = Train.objects.all()
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            train = Train.objects.get(pk=pk)
        except Train.DoesNotExist:
            return Response({"error": "Train not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TrainSerializer(train, data=request.data, partial=True)
        if serializer.is_valid():
            total_seats = serializer.validated_data.get('total_seats')
            if total_seats is not None:
                booked_seats = train.total_seats - train.available_seats
                if total_seats < booked_seats:
                    return Response({"error": "Total seats cannot be less than already booked seats."}, status=status.HTTP_400_BAD_REQUEST)
                serializer.validated_data['available_seats'] = total_seats - booked_seats

            serializer.save()
            return Response({"message": "Train updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            train = Train.objects.get(pk=pk)
        except Train.DoesNotExist:
            return Response({"error": "Train not found."}, status=status.HTTP_404_NOT_FOUND)

        train.delete()
        return Response({"message": "Train deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class SeatAvailabilityView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        if not source or not destination:
            return Response({"error": "Source and destination are required."},
                            status=status.HTTP_400_BAD_REQUEST)
        trains = Train.objects.filter(source__iexact=source, destination__iexact=destination)
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookSeatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    
    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            booking = serializer.save()
            return Response({"message": "Seat booked successfully.", "booking_id": booking.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    
    def get(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."},
                            status=status.HTTP_404_NOT_FOUND)
