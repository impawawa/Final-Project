from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs (Activity 1)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('protected/', views.protected_view, name='protected'),
    
    # Car CRUD URLs (Activity 2)
    path('cars/', views.car_list, name='car_list'),
    path('cars/create/', views.car_create, name='car_create'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('cars/<int:pk>/update/', views.car_update, name='car_update'),
    path('cars/<int:pk>/delete/', views.car_delete, name='car_delete'),
    
    # Rental CRUD URLs (Activity 2)
    path('rentals/', views.rental_list, name='rental_list'),
    path('rentals/create/', views.rental_create, name='rental_create'),
    path('rentals/<int:pk>/', views.rental_detail, name='rental_detail'),
    path('rentals/<int:pk>/update/', views.rental_update, name='rental_update'),
    path('rentals/<int:pk>/delete/', views.rental_delete, name='rental_delete'),
]
