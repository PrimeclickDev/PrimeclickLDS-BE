from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import AccountActivationSerializer, CustomTokenObtainPairSerializer, ForgotPasswordSerializer, NewPasswordSerializer, ResetPassowrdOTPSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
import datetime
import random

from .utils import send_otp_via_email, generate_otp

User = get_user_model()


class WelcomeAPIView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):
        return Response({"message": "Welcome to PrimeClick's AutoLeads Application. We are still in development!"})


class NewAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        return Response({"message": "Testing New page!"})


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Generate a six-digit OTP
        otp = generate_otp(length=6)
        print(otp)

        # # Sending the OTP
        send_otp_via_email(email, otp)

        # Save OTP in user model
        user = serializer.save(is_active=False)
        user.otp = otp
        user.save()
        print(user.id)
        business_id = user.business_id.id

        response_data = {
            "user_id": user.id,
            "business_id": business_id,
            "otp": otp,
            "message": "Your account activation OTP has been sent successfully"
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class ActivationAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = AccountActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['otp']
        user_id = serializer.validated_data['user_id']

        # Retrieve user by ID
        user = User.objects.filter(id=user_id, is_active=False).first()

        if user and user.otp == otp:
            # Activate user
            user.is_active = True
            user.save()

            return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid OTP. Please try again."}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserLogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "No refresh token provided."}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        user = User.objects.filter(
            email=email, is_active=True).first()

        # email = user.email

        if user is None:
            return Response({"message": "No active user found with the provided email."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a six-digit OTP
        otp = str(random.randint(100000, 999999))

        send_otp_via_email(email, otp)
        print(email, otp)

        # Save the OTP in the user's session
        request.session['reset_password_otp'] = otp

        response_data = {
            "user_id": user.id,
            "message": "Your reset password OTP has been sent successfully"
        }

        return Response(response_data, status=status.HTTP_200_OK)


class VerifyPasswordOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPassowrdOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['pass_otp']
        session_otp = request.session['reset_password_otp']

        if otp != session_otp:
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the verified OTP in the session
        request.session['verified_otp'] = session_otp

        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)


class NewPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        saved_otp = request.session.get('verified_otp')
        if saved_otp is None:
            return Response({"message": "OTP verification required."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        # Find the user with the verified OTP
        user = User.objects.filter(
            id=user_id, is_active=True).first()

        if user is None:
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the new passwords match
        if new_password != confirm_password:
            return Response({"message": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(new_password)
        # user.reset_password_otp = None
        user.save()

        # Clear the verified OTP from the session
        del request.session['verified_otp']

        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
