# HIRAM - Car Rental System API

A Django REST API for a car rental system that allows users to manage cars and rentals.

## Rate Limiting

The API implements rate limiting to prevent abuse and ensure fair usage. Rate limiting is applied per IP address.

### Rate Limit Rules
- All endpoints are limited to 5 requests per minute per IP address
- The limit resets after 60 seconds
- Rate limits are tracked separately for each endpoint

### Rate Limit Response
When the rate limit is exceeded, the API will return:
```json
{
    "error": "Rate limit exceeded",
    "detail": "Too many requests. Maximum 5 requests per 60 seconds."
}
```
Status Code: 429 Too Many Requests

### Example Rate Limit Scenarios

1. Login Attempts:
   - First 5 login attempts within a minute: Success (200 OK)
   - 6th attempt within the same minute: Rate limit error (429)

2. Car Operations:
   - First 5 requests to list/create/update/delete cars within a minute: Success
   - 6th request within the same minute: Rate limit error

3. Rental Operations:
   - First 5 requests to list/create/update/delete rentals within a minute: Success
   - 6th request within the same minute: Rate limit error

### Best Practices
- Implement exponential backoff when receiving 429 responses
- Cache responses when possible to reduce API calls
- Consider implementing request queuing for high-volume operations

## Authentication Endpoints

### Register User
- **Method**: POST
- **URL**: `/register/`
- **Request Body**:
  ```json
  {
      "username": "john_doe",
      "password": "secure_password123",
      "email": "john@example.com"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
      "message": "User registered successfully.",
      "token": "your.jwt.token"
  }
  ```

### Login User
- **Method**: POST
- **URL**: `/login/`
- **Request Body**:
  ```json
  {
      "username": "john_doe",
      "password": "secure_password123"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
      "token": "your.jwt.token"
  }
  ```

### Get JWT Token (Alternative)
- **Method**: POST
- **URL**: `/api/token/`
- **Request Body**:
  ```json
  {
      "username": "john_doe",
      "password": "secure_password123"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
      "access": "your.access.token",
      "refresh": "your.refresh.token"
  }
  ```

### Refresh JWT Token
- **Method**: POST
- **URL**: `/api/token/refresh/`
- **Request Body**:
  ```json
  {
      "refresh": "your.refresh.token"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
      "access": "your.new.access.token"
  }
  ```

## Car Endpoints

### List All Cars
- **Method**: GET
- **URL**: `/cars/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  ```
- **Response (200 OK)**:
  ```json
  [
      {
          "id": 1,
          "brand": "Toyota",
          "model": "Camry",
          "year": 2020,
          "price_per_day": 50.00,
          "description": "A reliable sedan",
          "owner": 1
      }
  ]
  ```

### Create Car
- **Method**: POST
- **URL**: `/cars/create/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "brand": "Toyota",
      "model": "Camry",
      "year": 2020,
      "price_per_day": 50.00,
      "description": "A reliable sedan"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
      "id": 1,
      "brand": "Toyota",
      "model": "Camry",
      "year": 2020,
      "price_per_day": 50.00,
      "description": "A reliable sedan",
      "owner": 1
  }
  ```

### Get Car Details
- **Method**: GET
- **URL**: `/cars/{id}/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  ```
- **Response (200 OK)**:
  ```json
  {
      "id": 1,
      "brand": "Toyota",
      "model": "Camry",
      "year": 2020,
      "price_per_day": 50.00,
      "description": "A reliable sedan",
      "owner": 1
  }
  ```

### Update Car
- **Method**: PUT
- **URL**: `/cars/{id}/update/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "brand": "Toyota",
      "model": "Camry",
      "year": 2021,
      "price_per_day": 75.00,
      "description": "Updated description"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
      "id": 1,
      "brand": "Toyota",
      "model": "Camry",
      "year": 2021,
      "price_per_day": 75.00,
      "description": "Updated description",
      "owner": 1
  }
  ```

### Delete Car
- **Method**: DELETE
- **URL**: `/cars/{id}/delete/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  ```
- **Response (200 OK)**:
  ```json
  {
      "message": "Car Toyota Camry has been successfully deleted"
  }
  ```

## Rental Endpoints

### List User's Rentals
- **Method**: GET
- **URL**: `/rentals/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  ```
- **Response (200 OK)**:
  ```json
  [
      {
          "id": 1,
          "car": 1,
          "user": 1,
          "start_date": "2024-05-01",
          "end_date": "2024-05-05"
      }
  ]
  ```

### Create Rental
- **Method**: POST
- **URL**: `/rentals/create/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "car": 1,
      "start_date": "2024-05-01",
      "end_date": "2024-05-05"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
      "id": 1,
      "car": 1,
      "user": 1,
      "start_date": "2024-05-01",
      "end_date": "2024-05-05"
  }
  ```

### Get Rental Details
- **Method**: GET
- **URL**: `/rentals/{id}/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  ```
- **Response (200 OK)**:
  ```json
  {
      "id": 1,
      "car": 1,
      "user": 1,
      "start_date": "2024-05-01",
      "end_date": "2024-05-05"
  }
  ```

### Update Rental
- **Method**: PUT
- **URL**: `/rentals/{id}/update/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "start_date": "2024-05-02",
      "end_date": "2024-05-06"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
      "id": 1,
      "car": 1,
      "user": 1,
      "start_date": "2024-05-02",
      "end_date": "2024-05-06"
  }
  ```

### Delete Rental
- **Method**: DELETE
- **URL**: `/rentals/{id}/delete/`
- **Headers**:
  ```
  Authorization: Bearer your.jwt.token
  ```
- **Response (204 No Content)**

## Error Responses

### Authentication Errors
- **401 Unauthorized**:
  ```json
  {
      "detail": "Authentication credentials were not provided."
  }
  ```
- **403 Forbidden**:
  ```json
  {
      "error": "You do not have permission to perform this action."
  }
  ```

### Not Found Error
- **404 Not Found**:
  ```json
  {
      "detail": "Not found."
  }
  ```

### Validation Error
- **400 Bad Request**:
  ```json
  {
      "field_name": [
          "Error message"
      ]
  }
  ``` 