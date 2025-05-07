Register a User
➤ Postman Configuration:
Method: POST

URL: http://127.0.0.1:8000/register/

Headers:

Content-Type: application/json

Body → select raw → choose JSON:

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secret123"
}

Expected Response:
{
  "message": "User registered successfully."
}

Login with Credentials
➤ Postman Configuration:
Method: POST

URL: http://127.0.0.1:8000/login/

Headers:

Content-Type: application/json

Body → select raw → choose JSON:

{
  "username": "johndoe",
  "password": "secret123"
}

Expected Response:
{
  "token": "your.jwt.token.here"
}

Access a Protected Route
➤ Postman Configuration:
Method: GET

URL: http://127.0.0.1:8000/protected/

Headers:

Authorization: Bearer your.jwt.token.here (paste your token from login)

Expected Response:
{
  "message": "Access granted to protected route"
}
