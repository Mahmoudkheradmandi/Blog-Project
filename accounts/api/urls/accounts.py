from django.urls import path 
from .. import views
 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    # registration
    path('registration/' , views.RegistrationApiView.as_view() , name='registration'),
    
    # Login Token
    # path('token/login' , ObtainAuthToken.as_view() , name='token-login'),
    path('token/login/' , views.CustomObtainAuthToken.as_view() , name='token-login'),
    path('token/logout/' , views.CustomDiscarAuthToken.as_view() , name='token-logout'),
    
    
    
    # activation 
    path("activation/confirm/<str:token>", views.ActivationApiView.as_view(), name="activation"),
    
    # Resend activation
    path("activation/resend/", views.ActivationResendApiView.as_view(), name="resend"),
    
    # chenge password
    path('change-password/' , views.ChangePasswordApiView.as_view() , name ='change-password'),    
        
    # JWT Token
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='custom-jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
    
    
]     