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


