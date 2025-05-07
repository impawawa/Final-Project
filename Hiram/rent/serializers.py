from rest_framework import serializers
from .models import Car, Rental
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CarSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'owner', 'brand', 'model', 'year', 'price_per_day', 
                 'description', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

class RentalSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    renter = UserSerializer(read_only=True)
    car_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Rental
        fields = ['id', 'car', 'car_id', 'renter', 'start_date', 'end_date',
                 'total_price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['renter', 'total_price', 'created_at', 'updated_at'] 