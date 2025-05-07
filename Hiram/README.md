# HIRAM - Car Rental System API

A Django REST API for a car rental system that allows users to manage cars and rentals.

## Authentication

All endpoints except registration and login require authentication using JWT tokens.

### Register User
- **Method**: POST
- **URL**: `/register/`
- **Headers**: 
  - Content-Type: application/json
- **Body**:
```json
{
    "username": "user123",
    "email": "user@example.com",
    "password": "yourpassword"
}
```
- **Response**:
```json
{
    "message": "User registered successfully."
}
```

### Login
- **Method**: POST
- **URL**: `/login/`
- **Headers**: 
  - Content-Type: application/json
- **Body**:
```json
{
    "username": "user123",
    "password": "yourpassword"
}
```
- **Response**:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Car Endpoints

### List All Cars
- **Method**: GET
- **URL**: `/cars/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token
- **Response**:
```json
[
    {
        "id": 1,
        "owner": {
            "id": 1,
            "username": "user123",
            "email": "user@example.com"
        },
        "brand": "Toyota",
        "model": "Camry",
        "year": 2020,
        "price_per_day": "50.00",
        "description": "Well maintained sedan",
        "is_available": true,
        "created_at": "2024-03-07T12:00:00Z",
        "updated_at": "2024-03-07T12:00:00Z"
    }
]
```

### Create Car
- **Method**: POST
- **URL**: `/cars/create/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token
  - Content-Type: application/json
- **Body**:
```json
{
    "brand": "Toyota",
    "model": "Camry",
    "year": 2020,
    "price_per_day": "50.00",
    "description": "Well maintained sedan"
}
```

### Get Car Details
- **Method**: GET
- **URL**: `/cars/{id}/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token

### Update Car
- **Method**: PUT
- **URL**: `/cars/{id}/update/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token
  - Content-Type: application/json
- **Body**:
```json
{
    "price_per_day": "55.00",
    "description": "Updated description"
}
```

### Delete Car
- **Method**: DELETE
- **URL**: `/cars/{id}/delete/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token

## Rental Endpoints

### List User's Rentals
- **Method**: GET
- **URL**: `/rentals/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token
- **Response**:
```json
[
    {
        "id": 1,
        "car": {
            "id": 1,
            "brand": "Toyota",
            "model": "Camry",
            "year": 2020
        },
        "renter": {
            "id": 1,
            "username": "user123",
            "email": "user@example.com"
        },
        "start_date": "2024-03-07",
        "end_date": "2024-03-10",
        "total_price": "150.00",
        "status": "active",
        "created_at": "2024-03-07T12:00:00Z",
        "updated_at": "2024-03-07T12:00:00Z"
    }
]
```

### Create Rental
- **Method**: POST
- **URL**: `/rentals/create/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token
  - Content-Type: application/json
- **Body**:
```json
{
    "car_id": 1,
    "start_date": "2024-03-07",
    "end_date": "2024-03-10"
}
```

### Get Rental Details
- **Method**: GET
- **URL**: `/rentals/{id}/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token

### Update Rental
- **Method**: PUT
- **URL**: `/rentals/{id}/update/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token
  - Content-Type: application/json
- **Body**:
```json
{
    "status": "completed"
}
```

### Delete Rental
- **Method**: DELETE
- **URL**: `/rentals/{id}/delete/`
- **Headers**: 
  - Authorization: Bearer your_jwt_token

## Error Responses

### Unauthorized (401)
```json
{
    "error": "Invalid credentials"
}
```

### Forbidden (403)
```json
{
    "error": "Not authorized"
}
```

### Not Found (404)
```json
{
    "detail": "Not found."
}
```

### Bad Request (400)
```json
{
    "field_name": ["Error message"]
}
``` 