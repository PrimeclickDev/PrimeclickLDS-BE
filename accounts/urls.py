from django.urls import path
# from .views import CustomUserCreateView
from django.urls import path
from .views import ForgotPasswordAPIView, NewPasswordAPIView, UserRegistrationAPIView, ActivationAPIView, VerifyPasswordOTPAPIView, WelcomeAPIView, NewAPIView, UserLogoutAPIView

urlpatterns = [
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('api/activate/', ActivationAPIView.as_view(), name='account-activation'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('verify-password-otp/', VerifyPasswordOTPAPIView.as_view(),
         name='verify-password-otp'),
    path('reset-password/', NewPasswordAPIView.as_view(), name='reset-password'),
    # path('auth/users/', CustomUserCreateView.as_view({'post': 'create'}), name='user-create'),
    path('home/', WelcomeAPIView.as_view(), name='welcome'),
    path('new/', NewAPIView.as_view(), name='new'),
]