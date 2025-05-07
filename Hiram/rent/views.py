import json
import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import RegisterForm, LoginForm
from .utils import generate_jwt
from django.contrib.auth.models import User

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = RegisterForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'User registered successfully.'})
        return JsonResponse({'errors': form.errors}, status=400)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = LoginForm(data)
        if form.is_valid():
            user = form.authenticate_user()
            if user:
                token = generate_jwt(user)
                return JsonResponse({'token': token})
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        return JsonResponse({'errors': form.errors}, status=400)

@csrf_exempt
def protected_view(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return JsonResponse({'message': 'Access granted to protected route'})
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)
