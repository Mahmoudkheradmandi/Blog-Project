from django.db import models
from accounts.models import *
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.urls import reverse


User = get_user_model()


class Post (models.Model):
    '''
    this is a class to define posts for blog app
    '''

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    image =  models.ImageField(null=True , blank=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL , null=True)
    pub_date = models.DateField()
    crea_date = models.DateField(auto_now_add=False)
    up_date = models.DateField(auto_now=False)
    
    def __str__(self):
        return self.title
    
    def get_snippet(self):
        return self.content[0:5]
    
    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})
    
    
    
    
class Category (models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name