from django.contrib.auth.backends import ModelBackend
from .models import User

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