from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from rest_framework import serializers

from main.models import *

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = SarayUser
        fields = [
            'email',
            'username',
            'password',
            'token',
        ]

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
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    sms_notification = serializers.BooleanField(read_only=True)
    bonus = serializers.CharField(read_only=True)
    bonus_amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = SarayUser
        fields = [
            'username',
            'password',
            'email',
            'phone',
            'image',
            'first_name',
            'last_name',
            'fathers_name',
            'birthdate',
            'passport_series',
            'passport_number',
            'insurance',
            'sms_notification',
            'mail_notification',
            'allow_to_use_photos',
            'bonus',
            'bonus_amount',
        ]


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

class LocationsExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleImageLocations
        fields = [
            'image',
        ]

class LocationsPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'image',
        ]

class LocationsDetailSerializer(serializers.ModelSerializer):
    example_images = LocationsExampleSerializer(source='examples', many=True, read_only=True)

    class Meta:
        model = Locations
        fields = [
            'id',
            'title',
            'text',
            'image',
            'cost',
            'over_week_cost',
            'over_time_cost',
            'example_images',
        ]

class PhotographsExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleImagePhotographs
        fields = [
            'image',
        ]

class PhotographsDetailSerializer(serializers.ModelSerializer):
    example_images = PhotographsExampleSerializer(source='examples', many=True, read_only=True)

    class Meta:
        model = Photographs
        fields = [
            'id',
            'first_name',
            'last_name',
            'desc',
            'link',
            'cost',
            'image',
            'example_images',
        ]

class NewsPreviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_short_name')

    class Meta:
        model = News
        fields = [
            'id',
            'author_name',
            'title',
            'desc',
            'image',
            'created_at',
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_short_name')

    class Meta:
        model = News
        fields = [
            'author_name',
            'title',
            'desc',
            'text',
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
        ]

class BookingsPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = [
            'id',
            'date',
            'time_start',
            'time_end',
            'location',
        ]

class BookingsRawPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleRawImageBookings
        fields = [
            'image',
        ]

class BookingsProcessedPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleProcessedImageBookings
        fields = [
            'image',
        ]

class BookingsDetailSerializer(serializers.ModelSerializer):
    booking_raw_photos = BookingsRawPhotosSerializer(source='photos_raw', many=True, read_only=True)
    booking_processed_photos = BookingsProcessedPhotosSerializer(source='photos_processed', many=True, read_only=True)

    class Meta:
        model = Bookings
        fields = [
            'id',
            'user',
            'date',
            'time_start',
            'time_end',
            'location',
            'photograph',
            'types',
            'options',
            'cost',
            'bonus_used',
            'booking_raw_photos',
            'booking_processed_photos',
            # 'contract',
        ]