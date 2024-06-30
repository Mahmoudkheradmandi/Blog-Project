from rest_framework import generics
from .serializers import (RegistrationSerializer , CustomAuthTokenSerializer , 
                        ActivationResendSerializer,  ChangePasswordApiSerializer , ProfileSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from accounts.models import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from jwt import ExpiredSignatureError , InvalidAudienceError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data={
                
                'email' : email
                
            }
            
            return Response (data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST) 
    
    def get_tokens_for_user(self , user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    
    
    
class CustomObtainAuthToken(ObtainAuthToken):    
    serializer_class = CustomAuthTokenSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })    
        
        
        
        
class CustomDiscarAuthToken(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self , request):
        request.user.auth_token.delete()
        print(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = CustomTokenObtainPairSerializer
    
    
    
class ChangePasswordApiView(generics.GenericAPIView):  
    
    model = User 
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordApiSerializer
    
    def get_object(self , required=None):
        obj = self.request.user
        return obj
 
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
         
        if serializer.is_valid():
                # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'details' : 'Password changed successfully'} , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
 
 
 
class ProfileApiView(generics.RetrieveUpdateAPIView):
        
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset , user = self.request.user)
        return obj
    

    
    
    
class ActivationApiView(APIView):
    
    def get(self, request,token, *args, **kwargs):
        
        #decode -> id_user
        print(token)
        try:
            token = jwt.decode(token , settings.SECRET_KEY , algorithms=['HS256'])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response({'detail' : 'This Token Signature'} , status=status.HTTP_400_BAD_REQUEST)
        except InvalidAudienceError:
            return Response({'detail' : 'This Token is Not Valid'} , status=status.HTTP_400_BAD_REQUEST)
            
        user_obj = User.objects.get(pk = user_id)
        if user_obj.is_verified :
            return Response ({'detail' : 'Your account have has already been verified'})
            
        user_obj.is_verified = True
        user_obj.is_active = True 
        user_obj.save()        
        return Response ({'detail' : 'Your account have has Verified and Activation successfully'})
        
        
        
        
class ActivationResendApiView(generics.GenericAPIView):
    
    serializer_class = ActivationResendSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)         
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        return Response({'detail' : 'user activation resend successfully'} , status=status.HTTP_200_OK) 

    def get_tokens_for_user(self , user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
