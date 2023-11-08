# from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from backend import settings
from business.models import Business
# from djoser.serializers import UserCreateSerializer
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'business_name', 'phone_number']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get('password')

        user = None

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            pass

        if user is not None:
            if user.check_password(password):
                refresh = self.get_token(user)  # Generate refresh token
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                # Serialize the user object using the UserSerializer
                user_serializer = UserSerializer(user)

                return {'access': access_token, 'refresh': refresh_token, 'user': user_serializer.data}

        raise serializers.ValidationError(_('Invalid credentials.'))


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=settings.MIN_PASSWORD_LENGTH)
    confirm_password = serializers.CharField(
        write_only=True, min_length=settings.MIN_PASSWORD_LENGTH)
    business_name = serializers.CharField(
        write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'business_name', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        business_name = validated_data.pop('business_name')
        validated_data['password'] = make_password(password)

        # Create a new Business instance and save it
        business, created = Business.objects.get_or_create(name=business_name)

        # Link the user to the business
        # validated_data['business'] = business

        user = User(**validated_data)
        user.business_id = business
        user.is_active = False
        user.save()

        return user


class AccountActivationSerializer(serializers.Serializer):
    otp = serializers.CharField(write_only=True, required=True)
    user_id = serializers.CharField(write_only=True, required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPassowrdOTPSerializer(serializers.Serializer):
    # user_id = serializers.CharField(write_only=True, required=True)
    pass_otp = serializers.CharField(required=True)


class NewPasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
