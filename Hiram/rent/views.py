import json
import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from .models import Car, Rental, UserProfile
from .serializers import CarSerializer, RentalSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .decorators import rate_limit
from .utils import generate_jwt
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

# Authentication Views
@csrf_exempt
@rate_limit(limit=5, period=60)  # 5 requests per minute for registration
def register_view(request):
    if request.method == 'POST':
        try:
            # Handle multipart form data
            if request.content_type.startswith('multipart/form-data'):
                form = RegisterForm(request.POST, request.FILES)
                if form.is_valid():
                    user = form.save()
                    # Handle photo upload
                    if 'photo' in request.FILES:
                        photo = request.FILES['photo']
                        # Check file size (2MB limit)
                        if photo.size > 2 * 1024 * 1024:  # 2MB in bytes
                            return JsonResponse({'error': 'Photo size must be less than 2MB'}, status=400)
                        # Create or update user profile
                        profile, created = UserProfile.objects.get_or_create(user=user)
                        profile.photo = photo
                        profile.save()
                    return JsonResponse({'message': 'User registered successfully.'})
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                # Handle JSON data
                data = json.loads(request.body)
                form = RegisterForm(data)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'message': 'User registered successfully.'})
                return JsonResponse({'errors': form.errors}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

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
    rentals = Rental.objects.filter(renter=request.user)
    serializer = RentalSerializer(rentals, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for rental creation
def rental_create(request):
    try:
        # Get the car
        car_id = request.data.get('car_id')
        if not car_id:
            return Response({'error': 'car_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        car = Car.objects.get(id=car_id)
        
        # Calculate total price
        start_date = datetime.strptime(request.data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.data.get('end_date'), '%Y-%m-%d').date()
        days = (end_date - start_date).days + 1  # Include both start and end dates
        total_price = float(car.price_per_day) * days
        
        # Create rental data
        rental_data = {
            'car_id': car_id,
            'start_date': start_date,
            'end_date': end_date,
            'total_price': str(total_price),  # Convert to string for DecimalField
            'status': 'pending'
        }
        
        serializer = RentalSerializer(data=rental_data)
        if serializer.is_valid():
            rental = serializer.save(renter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Car.DoesNotExist:
        return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        rental = Rental.objects.get(pk=pk, renter=request.user)
        
        # Get the car for price calculation
        car = rental.car
        
        # Get dates from request or use existing ones
        start_date = request.data.get('start_date', rental.start_date)
        end_date = request.data.get('end_date', rental.end_date)
        
        # Convert string dates to date objects if they're strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Calculate new total price
        days = (end_date - start_date).days + 1
        total_price = float(car.price_per_day) * days
        
        # Update rental data
        data = request.data.copy()
        data['total_price'] = str(total_price)
        
        serializer = RentalSerializer(rental, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Rental.DoesNotExist:
        return Response({'error': 'Rental not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@rate_limit(limit=5, period=60)  # 5 requests per minute for rental delete
def rental_delete(request, pk):
    try:
        rental = Rental.objects.get(pk=pk, renter=request.user)
        car_info = f"{rental.car.brand} {rental.car.model}"
        rental.delete()
        return Response(
            {'message': f'Rental for {car_info} has been successfully cancelled'},
            status=status.HTTP_200_OK
        )
    except Rental.DoesNotExist:
        return Response(
            {'error': 'Rental not found or you do not have permission to delete it'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
