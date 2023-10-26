from django.urls import path
from .views import WelcomeAPIView, NewAPIView

urlpatterns = [
    path('home/', WelcomeAPIView.as_view(), name='welcome'),
    path('new/', NewAPIView.as_view(), name='new'),
]