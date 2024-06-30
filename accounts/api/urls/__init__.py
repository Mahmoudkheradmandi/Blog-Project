from django.urls import path , include
from .. import views
# from rest_framework.authtoken.views import ObtainAuthToken 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    
    path('' , include('accounts.api.v1.urls.accounts')),
    path('profile/' , include('accounts.api.v1.urls.profiles')),
    
    
]