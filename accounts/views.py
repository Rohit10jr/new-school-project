from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.response import ResponseChoices
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_203_NON_AUTHORITATIVE_INFORMATION, HTTP_206_PARTIAL_CONTENT, 
    HTTP_500_INTERNAL_SERVER_ERROR)
from django.contrib.auth import get_user_model
User = get_user_model()
from .serializers import SigninSerializer,SignupSerializer, ProfileSerializer, UserCheckSerializer, UserDetailsSerializer
from rest_framework.authtoken.models import Token
from .auth_backend import PasswordlessAuthBackend

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from .models import Profile
from django.db.models import Q
from utils.pagination import Pagination
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.pagination import PageNumberPagination

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
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors, }, status=HTTP_400_BAD_REQUEST)


# class SimpleLoginView(APIView):
#     serializer_class = SigninSerializer
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         phone = request.data.get('phone')
#         if email and phone:
#             try:
#                 print(email, phone)
#                 user = PasswordlessAuthBackend.authenticate(
#                     request, email=email, phone=phone)
#                 # user = authenticate(
#                 #     request, email=email, phone=phone)
#                 login(request, user)
#                 print(user)
#             except Exception as e:
#                 return Response({"status": str(e)}, status=HTTP_204_NO_CONTENT)
#             if user:
#                 token, created = Token.objects.get_or_create(user=user)
#                 print(token)
#                 data = {
#                     "id": user.id,
#                     "token": token.key,
#                     "email": user.email,
#                     "phone": user.phone,
#                     "user_type": user.user_type,
#                     "data_entry": user.is_data_entry,
#                     "register_number": user.register_number
#                 }
#                 return Response({"status": ResponseChoices.SUCCESS, "data": data, "token":token.key}, status=HTTP_200_OK)
#         return Response({"status": "failed"}, status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class SimpleLoginView(APIView):
    serializer_class = SigninSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        
        if email and phone:
            try:
                print(email, phone)
                user = PasswordlessAuthBackend.authenticate(
                    request, email=email, phone=phone)
                
                if user is not None:
                    login(request, user)
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
                    return Response({"status": "success", "data": data, "token": token.key}, status=HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials"}, status=HTTP_401_UNAUTHORIZED)

            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "failed", "message": "Email and phone are required"}, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if self.request.user:
            logout(request)
            return Response({'status': ResponseChoices.LOGOUT}, status=HTTP_200_OK)
        return Response({'status': 'user doesn\'t logged in'}, status=HTTP_204_NO_CONTENT)



class StudentProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    def retrieve(self, request, pk):
        if self.request.user.user_type == 'is_student' and self.request.user.id == pk:
            queryset = get_object_or_404(Profile, user=pk)
        else:
            return Response({"status": 'failure', "message": "you don't have a permissions"}, status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request, pk):
        try:
            profile = Profile.objects.get(id=pk)
            print("before serializer")
            serializer = ProfileSerializer(profile, data=request.data)
            print("after serializer")
            if serializer.is_valid():
                print("valid serializer")
                serializer.save()
            return Response({'status': 'success','data': serializer.data}, status=HTTP_200_OK)

        except Exception as e:
            print("inside except")
            return Response({'status': 'failure', 'data': str(e)}, status=HTTP_400_BAD_REQUEST)


class UserDetailsView(ListAPIView, Pagination):
    serializer_class = UserDetailsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        standard = self.request.query_params.get('standard')
        user_type = (self.request.query_params.get('user_type'))
        user = self.request.user
        queryset = []
        if user.user_type != '':
            if user.user_type == 'is_student':
                queryset = User.objects.get(id=user.id)
            elif user.user_type == 'is_staff':
                staff_standard = user.profile.standard
                print(staff_standard)
                queryset = User.objects.all()
                queryset = User.objects.filter(
                    user_type='is_student', profile__standard__overlap=staff_standard)
                print(queryset)
            elif user.user_type == 'is_admin':
                queryset = User.objects.all()

            # for none student and without user type  
            if standard and user.user_type != 'is_student':
                queryset = queryset.filter(
                    profile__standard__overlap=[standard])
                if user_type:
                    queryset = queryset.filter(user_type=user_type)
                print(queryset)
        else:
            # for data_entry true
            if user.is_data_entry:
                queryset = User.objects.all()
                print(len(queryset))
        return queryset

    def list(self, request):
        try:
            user = request.user
            queryset = self.get_queryset()
            results = self.paginate_queryset(queryset)
            if user.user_type == 'is_student':
                serializer = UserDetailsSerializer(results)
            else:
                serializer = UserDetailsSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'status': 'failure', 'data': str(e)}, status=HTTP_204_NO_CONTENT)
        

class UserDetailsEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def retrieve(self, request, pk):
        try:
            requestuser = self.request.user
            if requestuser.id == pk:
                user = User.objects.get(pk=pk)
            else:
                if requestuser.user_type == 'is_admin':
                    user = User.objects.get(Q(user_type='is_staff', pk=pk) | Q(
                        user_type='is_student', pk=pk) | Q(is_data_entry=True, pk=pk))
                elif requestuser.user_type == 'is_staff':
                    user = User.objects.get(user_type='is_student', pk=pk)
            serializer = UserDetailsSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response({"status": "User doesn't exits or you don't have a permissions"}, status=HTTP_204_NO_CONTENT)
    

class ProfileView(APIView):
    # this are typically used in generic or viewset not in apiview
    # serializer_class = UserDetailsSerializer
    # queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request):
        user = self.request.user
        print("user", user)
        serializer = UserDetailsSerializer(user)
        return Response({"status": ResponseChoices.SUCCESS, "data": serializer.data}, status=HTTP_200_OK)

#AB
# class check_for_user(APIView):
#     serializer_class = UserDetailsSerializer
#     permission_classes = [AllowAny]

#     def get(self, request):
#         email = (self.request.query_params.get('email'))
#         phone = self.request.query_params.get('phone')
#         users = User.objects.all()
#         for i in users:
#             if phone and i.phone == phone:
#                 return Response(status=HTTP_200_OK)
#             if email and i.email == email.lower():
#                 return Response(status=HTTP_200_OK)
#         return Response(status=HTTP_404_NOT_FOUND)



#  Alternate serializers with better logic and practices
'''
class StudentProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        profile_user_id = kwargs.get('pk')
        
        if user.user_type == 'is_student' and user.id == int(profile_user_id):
            profile = get_object_or_404(Profile, user=profile_user_id)
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            raise PermissionDenied("You don't have permission to access this profile.")

    def update(self, request, *args, **kwargs):
        profile_user_id = kwargs.get('pk')
        user = request.user

        if user.user_type == 'is_student' and user.id == int(profile_user_id):
            profile = get_object_or_404(Profile, user=profile_user_id)
            serializer = self.get_serializer(profile, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You don't have permission to update this profile.")

class UserDetailsView(ListAPIView, PageNumberPagination):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        standard = self.request.query_params.get('standard')
        user_type = self.request.query_params.get('user_type')
        user = self.request.user

        # Default queryset
        queryset = User.objects.all()

        # Filter based on user type
        if user.user_type == 'is_student':
            queryset = queryset.filter(id=user.id)
        elif user.user_type == 'is_staff':
            staff_standard = user.profile.standard
            queryset = queryset.filter(user_type='is_student', profile__standard__overlap=staff_standard)
        elif user.user_type == 'is_admin':
            pass  # No additional filtering for admins

        # Additional filtering
        if standard and user.user_type != 'is_student':
            queryset = queryset.filter(profile__standard__overlap=[standard])
        if user_type:
            queryset = queryset.filter(user_type=user_type)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'status': 'failure', 'data': str(e)}, status=HTTP_400_BAD_REQUEST)


class UserDetailsEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        try:
            requestuser = self.request.user
            user_id = self.kwargs.get('pk')
            user = User.objects.get(pk=user_id)

            # Permission checks
            if requestuser.id != user_id:
                if requestuser.user_type == 'is_admin':
                    if not (user.user_type in ['is_staff', 'is_student'] or user.is_data_entry):
                        raise PermissionDenied("You do not have permission to access this user.")
                elif requestuser.user_type == 'is_staff' and user.user_type != 'is_student':
                    raise PermissionDenied("You do not have permission to access this user.")

            return user
        except User.DoesNotExist:
            raise Http404("User does not exist.")

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailsSerializer(user)
        return Response({"status": ResponseChoices.SUCCESS, "data": serializer.data}, status=HTTP_200_OK)

'''
# class check_for_user(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         email = self.request.query_params.get('email')
#         phone = self.request.query_params.get('phone')

#         if phone:
#             if User.objects.filter(phone=phone).exists():
#                 return Response({"status": "User with this phone number exists."}, status=HTTP_200_OK)
        
#         if email:
#             if User.objects.filter(email=email.lower()).exists():
#                 return Response({"status": "User with this email exists."}, status=HTTP_200_OK)

#         return Response({"status": "No user found with the given email or phone number."}, status=HTTP_404_NOT_FOUND)


class check_for_user(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone = serializer.validated_data.get('phone')

        # If both phone and email are present, check for both
        if phone and email:
            user_exists = User.objects.filter(phone=phone, email=email.lower()).exists()
            if user_exists:
                return Response({"status": "User with this email and phone exists."}, status=HTTP_200_OK)
            else:
                return Response({"status": "No user found with the given email and phone."}, status=HTTP_404_NOT_FOUND)

        if phone and User.objects.filter(phone=phone).exists():
            return Response({"status": "User with this phone number exists."}, status=HTTP_200_OK)
        
        if email and User.objects.filter(email=email.lower()).exists():
            return Response({"status": "User with this email exists."}, status=HTTP_200_OK)

        return Response({"status": "No user found with the given email or phone number."}, status=HTTP_404_NOT_FOUND)