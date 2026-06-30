from urllib import request

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer
from .models import User
from .auth import generate_token, check_password
from .models import BlacklistedToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(
            email=data["email"],
            password=data["password"],
            last_name=data["last_name"],
            first_name=data["first_name"],
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"detail": "Incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({"detail": "Incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_token(user.id)
        return Response({"token": token})

@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(APIView):
    def get(self, request):

        if not request.jwt_user or not request.jwt_user.is_authenticated:
            return Response({"detail": "User is not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if UserSerializer(request.jwt_user).data.get('role') == 1:            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            users = User.objects.filter(is_staff=False)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

        return Response(UserSerializer(request.jwt_user).data)

    def put(self, request):
        if not request.jwt_user or not request.jwt_user.is_authenticated:
            return Response({"detail": "User is not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.jwt_user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        if not request.jwt_user or not request.jwt_user.is_authenticated:
            return Response({"detail": "User is not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        request.jwt_user.is_active = False
        request.jwt_user.save()
        return Response({"detail": "Account deactivated"}, status=status.HTTP_204_NO_CONTENT)
    

@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    def post(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"detail": "User is not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ")[1]
        BlacklistedToken.objects.get_or_create(token=token)
        return Response({"detail": "You are logged out of the system"}, status=status.HTTP_200_OK)
