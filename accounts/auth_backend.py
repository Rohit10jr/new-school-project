from django.contrib.auth.backends import ModelBackend
from .models import User

from django.contrib.auth import get_user_model
from django.db.models import Q

# class PasswordlessAuthBackend(ModelBackend):
#     def authenticate(self, email=None, phone=None):
#         try:
#             user = User.objects.get(email=email)
#             if user.check_password(phone):
#                 return user
#         except User.DoesNotExist:
#             return None


# class PasswordlessAuthBackend(ModelBackend):
#     def authenticate(self, email=None, phone=None):
#         try:
#             user = User.objects.get(email=email, phone=phone)
#             if user.check_password(phone):
#                 return user
#             return None
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None



# This is for having two different user id either phone or email id
'''

class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(email=username) | Q(phone=username))
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

'''


# default

class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, email,phone):
        try:
            return User.objects.get(email=email,phone=phone)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None