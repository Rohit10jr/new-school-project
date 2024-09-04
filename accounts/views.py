from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.response import ResponseChoices
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_203_NON_AUTHORITATIVE_INFORMATION, HTTP_206_PARTIAL_CONTENT
)
from django.contrib.auth import get_user_model
User = get_user_model()
from .serializers import SigninSerializer,SignupSerializer
from rest_framework.authtoken.models import Token
from .auth_backend import PasswordlessAuthBackend
# Create your views here.

# rohit@mail.com 6374851119

class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, "message": f"User {serializer.validated_data.pop('first_name')} Registered Successfully"}, status=HTTP_201_CREATED)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors, }, status=HTTP_206_PARTIAL_CONTENT)


class SimpleLoginView(APIView):
    serializer_class = SigninSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        if email and phone:
            try:
                user = PasswordlessAuthBackend.authenticate(
                    request, email=email, phone=phone)
                # user = authenticate(
                #     request, email=email, phone=phone)
                login(request, user)
                print(user)
            except Exception as e:
                return Response({"status": str(e)}, status=HTTP_204_NO_CONTENT)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    "id": user.id,
                    "token": token.key,
                    "email": user.email,
                    "phone": user.phone,
                    "user_type": user.user_type,
                    "data_entry": user.is_data_entry,
                    "register_number": user.register_number
                }
                return Response({"status": ResponseChoices.SUCCESS, "data": data}, status=HTTP_200_OK)
        return Response({"status": "failed"}, status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if self.request.user:
            logout(request)
            return Response({'status': ResponseChoices.LOGOUT}, status=HTTP_200_OK)
        return Response({'status': 'user doesn\'t logged in'}, status=HTTP_204_NO_CONTENT)

