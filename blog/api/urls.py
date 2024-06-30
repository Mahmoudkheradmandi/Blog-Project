from django.urls import path , include
from . import views
from blog.api.views import *
from rest_framework.routers import DefaultRouter


app_name = 'api-v1'

router = DefaultRouter()
router.register('post' , PostModelViewSet , basename='post')
router.register('category' , CategoryModelViewSet , basename='category')

urlpatterns = router.urls

