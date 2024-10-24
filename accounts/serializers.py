from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from backend import settings
from business.models import Business

User = get_user_model()


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    businesses = BusinessSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'businesses']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get(self.username_field).lower()
        password = attrs.get('password')

        user = None

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            pass

        if user is not None:
            if user.check_password(password):
                refresh = self.get_token(user)
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
                  'password', 'business_name', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        business_name = validated_data.pop('business_name')
        validated_data['password'] = make_password(password)
        validated_data['email'] = validated_data['email'].lower()

        # Create a new Business instance and save it

        # Link the user to the business
        user = User(**validated_data)
        user.is_active = False
        user.save()
        business = Business.objects.create(name=business_name)
        business.users.add(user)

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
