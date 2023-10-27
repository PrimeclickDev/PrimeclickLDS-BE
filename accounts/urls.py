from django.urls import path
from .views import WelcomeAPIView, NewAPIView
from .views import CustomUserCreateView

urlpatterns = [
    path('auth/users/', CustomUserCreateView.as_view({'post': 'create'}), name='user-create'),
    path('home/', WelcomeAPIView.as_view(), name='welcome'),
    path('new/', NewAPIView.as_view(), name='new'),
]