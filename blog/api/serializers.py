from rest_framework import serializers
from blog.models import Post , Category
from accounts.models import Profile



class PostSerializer(serializers.ModelSerializer):
    

    snippet = serializers.ReadOnlyField(source = 'get_snippet')
    relative_url = serializers.URLField(source = 'get_absolute_api_url' , read_only = True)
    absolute_url = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(      
        many=False,
        queryset = Category.objects.all(),
        read_only= False,
        slug_field='name'    
    )
    
    
    class Meta :
        model = Post
        fields = [
            'id' , 'author' , 'title', 'category' , 'status' , 
            'content' , 'crea_date' , 'pub_date' ,'up_date',
            'image' ,'relative_url', 'snippet' , 'absolute_url'
            
            ]
        
        read_only_fields = ['author']
        
    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
            
    def to_representation(self, instance):
        request = self.context.get('request')
        # print(request.__dict__)
        rep = super().to_representation(instance)   
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet' , None)
            rep.pop('absolute_url' , None)
            rep.pop('relative_url' , None)
            
            
        else :
            rep.pop('content' , None)
            
        rep['category'] = CategorySerializer(instance.category , context={'request' : request}).data
        return rep
      
      
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)  
    
class CategorySerializer(serializers.ModelSerializer):

    class Meta :
        model = Category
        fields = ['id' , 'name']   
      
      
      