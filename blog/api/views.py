
from rest_framework.permissions import IsAuthenticated 
from .serializers import PostSerializer , CategorySerializer
from ..models import Post ,Category
from blog.api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from .paginations import DefaultPagination
from rest_framework import viewsets



class PostModelViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated  , IsOwnerOrReadOnly]
    serializer_class = PostSerializer 
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_fields = ['author', 'category' , 'status']
    search_fields = ['=title','title', 'content']
    ordering_fields = ['pub_date' , 'author']
    pagination_class = DefaultPagination
    
    

class CategoryModelViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer 
    queryset = Category.objects.all()    
    