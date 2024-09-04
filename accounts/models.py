from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from datetime import datetime
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, MaxValueValidator


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, user_type, date_of_birth, register_number, password=None, is_data_entry=False, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone=phone,
            user_type=user_type,
            date_of_birth=date_of_birth,
            register_number=register_number,
            is_data_entry=is_data_entry, 
            **extra_fields         
        )

        user.set_password(phone or password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, user_type, date_of_birth, register_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone, user_type, date_of_birth, register_number, password, **extra_fields)
    
    # def create_superuser(self, email, phone, user_type, date_of_birth, register_number, password=None):
        # user = self.create_user(email, phone, user_type, date_of_birth, register_number, password)
        # user.is_staff = True
        # user.is_superuser = True
        # user.is_active = True  # Usually, superusers should be active
        # user.save(using=self._db)
        # return user


usertype_choice = (
    ('is_student', 'is_student'),
    ('is_staff', 'is_staff'),
    ('is_admin', 'is_admin'),
    )

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_data_entry = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    register_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)
    user_type = models.CharField(max_length=20,choices=usertype_choice,default=None,blank=True,null=True)
    phone = models.CharField(unique=True, default=1234567890, max_length=10, validators=[MinLengthValidator(10)])

    # admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'user_type', 'date_of_birth', 'register_number']

    def save(self, *args, **kwargs):
        if self.pk:  
            original = User.objects.get(pk=self.pk)
            if original.phone != self.phone:
                self.set_password(self.phone)
        else:  
            self.set_password(self.phone)

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ('created_at',)


class Profile(models.Model):
    def upload_design_to(self, filename):
        return f'user_profile/{self.user.id}/{filename}'
    # null=True: Profile can exist without being associated with a User, this is generally not recommended unless there's a specific use case for it.
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    full_name = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=45, blank=True, null=True)
    standard = ArrayField(
        models.CharField(max_length=10, blank=True),
        blank=True, default=list)
    profile_picture = models.ImageField(
        upload_to=upload_design_to, blank=True, null=True, default='user_profile/profile.png')
    
    def __str__(self):
        return str(self.user)

