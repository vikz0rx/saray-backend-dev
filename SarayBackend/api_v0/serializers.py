from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from main.models import News, SarayUser


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

class NewsPreviewSerializer(serializers.ModelSerializer):
   class Meta:
       model = News
       fields = [
           'id',
           'title',
           'image',
           'created_at',
           'url',
       ]


class NewsDetailSerializer(serializers.ModelSerializer):
   class Meta:
       model = News
       fields = [
           'title',
           'image',
           'created_at',
           'url',
       ]