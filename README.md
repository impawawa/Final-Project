### Register User
- **Method**: POST
- **URL**: `/register/`
- **Content-Type**: `multipart/form-data` or `application/json`
- **Request Body**:
  ```json
  // For JSON request:
  {
      "username": "john_doe",
      "password": "secure_password123",
      "email": "john@example.com"
  }

  // For multipart/form-data (with photo):
  {
      "username": "john_doe",
      "password": "secure_password123",
      "email": "john@example.com",
      "photo": [binary file data]
  }
  ```
- **Photo Requirements**:
  - File size: Maximum 2MB
  - Allowed formats: jpg, jpeg, png, webp
  - Image will be automatically cropped to 1:1 aspect ratio
- **Response (200 OK)**:
  ```json
  {
      "message": "User registered successfully."
  }
  ```
- **Error Responses**:
  ```json
  // File too large
  {
      "error": "Photo size must be less than 2MB"
  }

  // Invalid file type
  {
      "errors": {
          "photo": ["File extension 'pdf' is not allowed. Allowed extensions are: 'jpg', 'jpeg', 'png', 'webp'."]
      }
  }
  ```
