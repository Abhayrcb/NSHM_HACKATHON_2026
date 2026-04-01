from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
# Create your views here.
def get_token_for_user(user):
    if not user.is_active:
        raise AuthenticationFailed("User account is not activate yet")
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
class RegisterUserView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token =  get_token_for_user(user)
            res = {
                "success":True,
                "message":"Successfully Registered",
                "data":serializer.data,
                "access_token":token['access'],
                "errors":None
            }
            return Response(res,status=status.HTTP_201_CREATED)
        res = {
                "success":False,
                "message":"Registeration failed",
                "data":serializer.data,
                "access_token":None,
                "errors":serializer.errors
            }
        return Response(res,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        # print(request.data.get("email"),request.data.get("password"))
        user = authenticate(request,email=request.data.get("email"),password=request.data.get("password"))
        print(user)
        if user is not None:
            token = get_token_for_user(user)
            res = {
                "success":True,
                "message":"Successfully Login",
                "data":{
                    "user_id":user.id,
                    "email":user.email
                    },
                "access_token":token['access'],
                "errors":None
            }
            return Response(res,status=status.HTTP_200_OK)
        res = {
                "success":False,
                "message":"Invalid Credential",
                "data":None,
                "access_token":None,
                "errors":None
            }
        return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        print(request.user)
        print(request.headers)
        return Response({"msg":"hello from dashboard"})