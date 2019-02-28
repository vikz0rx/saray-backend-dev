from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from main.models import *

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = SarayUser
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        user = SarayUser.objects.create_user(**validated_data)
        customer = Group.objects.get(name='saray_customer')
        customer.user_set.add(user)
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = SarayUser
        fields = ('email', 'username', 'password', 'token',)
        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

class LocationsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = [
            'title',
            'text',
            'image',
            'cost',
        ]

class PhotographsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographs
        fields = [
            'first_name',
            'last_name',
            'desc',
            'link',
            'image',
        ]

class NewsPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id',
            'author',
            'title',
            'image',
            'created_at',
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'author',
            'title',
            'image',
            'created_at',
        ]

class BookingTypesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTypes
        fields = [
            'title',
            'desc',
            'cost',
        ]

class BookingOptionsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingOptions
        fields = [
            'title',
            'desc',
            'cost',
        ]

class BookingsRentTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = [
            'date',
            'time_start',
            'time_end',
            'status',
        ]

class BookingsPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = [
            'date',
            'time_start',
            'time_end',
            'location',
            'status',
        ]

class BookingsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = [
            'date',
            'time_start',
            'time_end',
            'status',
            'location',
            'photograph',
            'types',
            'options',
            'cost',
        ]