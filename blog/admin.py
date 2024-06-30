from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['author' , 'title' , 'category' , 'pub_date']

admin.site.register(Category)
admin.site.register(Post)
