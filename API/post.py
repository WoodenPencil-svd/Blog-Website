from rest_framework import views, generics, serializers, status
from rest_framework.response import Response

from API.helpers import get_paginated_response, LimitOffsetPagination
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from use_case.selector.post import PostSelector
from use_case.service.post import PostService

from a_posts.models import Tag


class PostListApi(views.APIView):
    http_method_names =['get']
    class OutPutSerializer(serializers.Serializer):
        title  = serializers.CharField()
        artist = serializers.CharField()
        url = serializers.CharField()
        image = serializers.URLField()
        author = serializers.CharField()
        body = serializers.CharField()
        tags =  serializers.StringRelatedField(many=True) 
        created = serializers.DateTimeField()
        id = serializers.CharField()
        
    def get(self,request,*args, **kwargs):
        data = PostSelector.list(self)
        ouput = self.OutPutSerializer(data,many=True).data
        return Response(ouput,status=status.HTTP_200_OK)
    
class PostRetriveApi(views.APIView):
    http_method_names = ['get']
    class OutPutSerializer(serializers.Serializer):
        title  = serializers.CharField()
        artist = serializers.CharField()
        url = serializers.CharField()
        image = serializers.URLField()
        author = serializers.CharField()
        body = serializers.CharField()
        tags =  serializers.StringRelatedField(many=True) 
        created = serializers.DateTimeField()
        id = serializers.CharField()
        
    def get(self,request, pk ,*args, **kwargs):
        data = PostSelector.get_by_id(self, id=pk)
        ouput = self.OutPutSerializer(data).data
        return Response(ouput,status=status.HTTP_200_OK)
    
    
class PostOfUserApi(views.APIView):
    http_method_names = ['get']
    class OutPutSerializer(serializers.Serializer):
        title  = serializers.CharField()
        artist = serializers.CharField()
        url = serializers.CharField()
        image = serializers.URLField()
        author = serializers.CharField()
        body = serializers.CharField()
        tags =  serializers.StringRelatedField(many=True) 
        created = serializers.DateTimeField()
        id = serializers.CharField()
        
    def get(self,request, pk ,*args, **kwargs):
        data = PostSelector.get_post_by_user_id(self, id=pk)
        ouput = self.OutPutSerializer(data,many=True).data
        return Response(ouput,status=status.HTTP_200_OK)
    
class PostCreateApi(views.APIView):
    http_method_names  = ['post']
    class OutPutSerializer(serializers.Serializer):
        title  = serializers.CharField()
        artist = serializers.CharField()
        url = serializers.CharField()
        image = serializers.URLField()
        author = serializers.CharField()
        body = serializers.CharField()
        tags =  serializers.StringRelatedField(many=True) 
        created = serializers.DateTimeField()
        id = serializers.CharField()
        
    class InPutSerializer(serializers.Serializer):
        title  = serializers.CharField()
        artist = serializers.CharField()
        url = serializers.CharField()
        image = serializers.URLField()
        author_id = serializers.IntegerField()
        body = serializers.CharField()
        tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='slug'  )
    
        
    def post(self,request,*args, **kwargs):
        input_data = self.InPutSerializer(data = request.data)
        input_data.is_valid(raise_exception=True)
        post = PostService.create(self,input=input_data.validated_data)
        post_id = PostSelector.get_by_id(self, id= post.id)
        data = self.OutPutSerializer(post_id).data
        return Response(data,status=status.HTTP_201_CREATED)

class PostUpdateApi(views.APIView):
    http_method_names  = ['put']
        
    class OutPutSerializer(serializers.Serializer):
        title  = serializers.CharField()
        artist = serializers.CharField()
        url = serializers.CharField()
        image = serializers.URLField()
        author = serializers.CharField()
        body = serializers.CharField()
        tags =  serializers.StringRelatedField(many=True) 
        created = serializers.DateTimeField()
        id = serializers.CharField()
        
    class InPutSerializer(serializers.Serializer):
        title  = serializers.CharField(required = False)
        artist = serializers.CharField(required = False)
        url = serializers.CharField(required = False)
        image = serializers.URLField(required = False)
        author_id = serializers.IntegerField(required = False)
        body = serializers.CharField(required = False)
        tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='slug',
        required = False
    )
        
    def post(self,request,*args, **kwargs):
        input_data = self.InPutSerializer(data = request.data)
        input_data.is_valid(raise_exception=True)
        post = PostService.update(self,input_data.validated_data)
        post_id = PostSelector.get_by_id(self, id= post.id)
        data = self.OutPutSerializer(post_id).data
        return Response(data,status=status.HTTP_200_OK)
    
class PostDeleteApi(generics.DestroyAPIView):
    http_method_names = ['delete']
    def delete(self,request,pk,*args, **kwargs):
        try:
            PostService.delete(self,id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
    
    