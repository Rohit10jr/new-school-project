from rest_framework import serializers
from django.shortcuts import get_list_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import User
from django.conf import settings

User  = get_user_model()

usertype_choice = (
    (None, '-------'),
    ('is_student', 'is_student'),
    ('is_staff', 'is_staff'),
    ('is_admin', 'is_admin'),
)

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=10, required=True)
    register_number = serializers.CharField(max_length=15, required=True)
    date_of_birth = serializers.DateField(required=True)
    user_type = serializers.ChoiceField(choices=usertype_choice, allow_blank=True, default=None, required=False)

    first_name = serializers.CharField(max_length=15, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=15, required=False, allow_blank=True)
    full_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    address = serializers.CharField(max_length=45, required=False, allow_blank=True)
    is_data_entry = serializers.BooleanField(required=False, default=False)
    standard = serializers.ListField(child=serializers.CharField(default=None), default=None, required=False)
    profile_picture = serializers.ImageField(
        required=False, max_length=None, allow_empty_file=True, use_url=True, default='user_profile/profile.png'
    )

    def create(self, validated_data):
        email = validated_data.pop("email").lower()
        phone = validated_data.pop("phone")
        register_number = validated_data.pop("register_number")
        date_of_birth = validated_data.pop("date_of_birth")
        user_type = validated_data.get("user_type")
        is_data_entry = validated_data.get("is_data_entry")
        
        first_name = validated_data.get("first_name", "")
        last_name = validated_data.get("last_name", "")
        full_name = validated_data.get("full_name", "")
        address = validated_data.get("address", "")
        standard = validated_data.get("standard", [])
        profile_picture = validated_data.get("profile_picture", 'user_profile/profile.png')

        user = User.objects.create_user(
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            user_type=user_type,
            register_number=register_number,
            is_data_entry=is_data_entry,
            password=phone
        )

        # user.first_name = first_name
        # user.last_name = last_name
        # user.full_name = full_name
        # user.address = address
        # user.standard = standard
        # user.profile_picture = profile_picture

        user.save()
        return user

    def validate(self, data):
        queryset = User.objects.all()
        if queryset.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'email already exists'})
        elif queryset.filter(phone=data['phone']).exists():
            raise serializers.ValidationError(
                {'error': 'phone already exists'})
        return data


'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'phone', 'register_number', 'date_of_birth',
            'user_type', 'first_name', 'last_name', 'full_name',
            'address', 'is_data_entry', 'standard', 'profile_picture'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Use create_user method to set the phone number as the password
        user = User.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            register_number=validated_data['register_number'],
            date_of_birth=validated_data['date_of_birth'],
            user_type=validated_data.get('user_type'),
            
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            full_name=validated_data.get('full_name', ''),
            address=validated_data.get('address', ''),
            is_data_entry=validated_data.get('is_data_entry', False),
            standard=validated_data.get('standard', []),
            profile_picture=validated_data.get('profile_picture', 'user_profile/profile.png')
        )
        return user
'''


class SigninSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone']