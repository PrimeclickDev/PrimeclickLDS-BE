from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from djoser.views import UserViewSet
from .serializers import UserCreateSerializer



class CustomUserCreateView(UserViewSet):
    serializer_class = UserCreateSerializer



class WelcomeAPIView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        return Response({"message": "Welcome to PrimeClick's AutoLeads Application. We are still in development!"})
    

class NewAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        return Response({"message": "Testing New page!"})
    
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer