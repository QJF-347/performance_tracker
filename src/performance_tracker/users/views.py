from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


from .serializers import RegisterSerializer, UserProfileSerializer


User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message":"Registration successfull"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny, ]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh":str(refresh), 
                "access":str(refresh.access_token), 
                "user":{
                    "id":user.id, 
                    "username":user.username, 
                    "email":user.email, 
                    "role":user.role
                }
            })
        else:
            return Response(
                {"error":"Invalid credentials"}, 
                status=status.HTTP_401_UNAUTHORIZED
                )

class LogoutView(APIView):
    permission_classes =[IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")  # Use `.get()` to avoid KeyError
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            
            return Response({"message": "Logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user