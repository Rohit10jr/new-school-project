from rest_framework import serializers
from django.shortcuts import get_list_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import User, Profile
from django.conf import settings
from django.core.exceptions import ValidationError

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
    is_data_entry = serializers.BooleanField(required=False, default=False)

    first_name = serializers.CharField(max_length=15)
    last_name = serializers.CharField(max_length=15)
    full_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    address = serializers.CharField(max_length=45, required=False, allow_blank=True)
    # standard = serializers.ListField(child=serializers.CharField(default=None), default=None, required=False)
    standard = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        required=False,
        default=list
    )
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

        if user_type == "is_admin":
            register_number=''

        user = User.objects.create_user(
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            user_type=user_type,
            register_number=register_number,
            is_data_entry=is_data_entry,
            password=phone
        )

        Profile.objects.create(
            user=user, 
            first_name=first_name, 
            last_name=last_name,  
            full_name=full_name,                                   
            standard=standard, 
            address=address,  
            profile_picture=profile_picture,
        )

        # userdetails = (
        #     email, phone, user_type, 
        #     first_name, last_name, full_name,
        #     date_of_birth, standard, address, 
        #     profile_picture, is_data_entry
        # )

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


# normal signin serializer
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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'full_name', "profile_picture", "standard", "address"]


class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    # to change dd-mm-yyyy format into yyyy-mm-dd format
    date_of_birth = serializers.DateField(input_formats=['%d-%m-%Y'], format='%Y-%m-%d', required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'register_number', 'date_of_birth', 
                  'is_active', 'user_type', 'created_at', 'profile']
        read_only_fields = ['id', 'created_at', 'user_type', 'is_data_entry']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.register_number = validated_data.get('register_number', instance.register_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        instance.save()

        profile.first_name = profile_data.get('first_name', profile.first_name)
        profile.last_name = profile_data.get('last_name', profile.last_name)
        profile.full_name = profile_data.get('full_name', profile.full_name)
        profile.standard = profile_data.get('standard', profile.standard)
        profile.address = profile_data.get('address', profile.address)
        # profile.section = profile_data.get('section', profile.section)

        profile.save()
        return instance


class UserCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, max_length=10)

    def validate(self, data):
        email = data.get('email')
        phone = data.get('phone')

        if not email and not phone:
            raise serializers.ValidationError("Either email or phone must be provided.")

        return data


