from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Train, Booking
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import F


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Unable to login with provided credentials.")

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ('id', 'train_number', 'source', 'destination', 'total_seats', 'available_seats')

class BookingSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)
    train_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'user', 'train', 'train_id', 'booking_time')
        read_only_fields = ('id', 'user', 'train', 'booking_time')
    
    def create(self, validated_data):
        user = self.context['request'].user
        train_id = validated_data.pop('train_id')

        try:
            with transaction.atomic():
                train = Train.objects.select_for_update().get(id=train_id)
                
                if train.available_seats <= 0:
                    raise serializers.ValidationError("No seats available on this train.")
                
                train.available_seats = F('available_seats') - 1
                train.save()

                train.refresh_from_db()

                booking = Booking.objects.create(user=user, train=train)
                return booking

        except Train.DoesNotExist:
            raise serializers.ValidationError("Train does not exist.")
