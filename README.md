A Django REST API for a car rental system that allows users to manage cars and rentals.
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
- - **Request Body**:
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
