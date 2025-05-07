import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from .models import Car, Rental
from .serializers import CarSerializer, RentalSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .decorators import rate_limit

# Authentication Views
@csrf_exempt
@rate_limit(limit=5, period=60)  # 5 requests per minute for registration
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = RegisterForm(data)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': 'User registered successfully.',
                'token': str(refresh.access_token)
            })
        return JsonResponse({'errors': form.errors}, status=400)

@csrf_exempt
@rate_limit(limit=5, period=60)  # 5 requests per minute for login
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = LoginForm(data)
            if form.is_valid():
                user = form.authenticate_user()
                if user:
                    refresh = RefreshToken.for_user(user)
                    return JsonResponse({
                        'token': str(refresh.access_token)
                    })
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for protected view
def protected_view(request):
    return JsonResponse({'message': 'Access granted to protected route'})

# Car CRUD Views
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for car list
def car_list(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for car creation
def car_create(request):
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for car detail
def car_detail(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CarSerializer(car)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for car update
def car_update(request, pk):
    try:
        car = Car.objects.get(pk=pk)
        # Check if the user is the owner of the car
        if car.owner != request.user:
            return Response(
                {'error': 'You do not have permission to update this car'},
                status=status.HTTP_403_FORBIDDEN
            )
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CarSerializer(car, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for car delete
def car_delete(request, pk):
    try:
        car = Car.objects.get(pk=pk)
        # Check if the user is the owner of the car
        if car.owner != request.user:
            return Response(
                {'error': 'You do not have permission to delete this car'},
                status=status.HTTP_403_FORBIDDEN
            )
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    car.delete()
    return Response(
        {'message': f'Car {car.brand} {car.model} has been successfully deleted'},
        status=status.HTTP_200_OK
    )

# Rental CRUD Views
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for rental list
def rental_list(request):
    rentals = Rental.objects.filter(user=request.user)
    serializer = RentalSerializer(rentals, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for rental creation
def rental_create(request):
    request.data['user'] = request.user.id
    serializer = RentalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for rental detail
def rental_detail(request, pk):
    try:
        rental = Rental.objects.get(pk=pk, user=request.user)
    except Rental.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = RentalSerializer(rental)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for rental update
def rental_update(request, pk):
    try:
        rental = Rental.objects.get(pk=pk, user=request.user)
    except Rental.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = RentalSerializer(rental, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for rental delete
def rental_delete(request, pk):
    try:
        rental = Rental.objects.get(pk=pk, user=request.user)
    except Rental.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    rental.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
