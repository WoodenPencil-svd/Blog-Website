from a_posts.models import Post
from django.shortcuts import  get_object_or_404
from uuid import UUID
class PostSelector:
    def list(self,):
        return Post.objects.all()
    
    def get_by_id(self, id , *args, **kwargs):
        id = UUID(str(id))
        post = get_object_or_404(Post,pk=id)
        return post
    
    def get_post_by_user_id(self, id,*args, **kwargs):
        return Post.objects.filter(author__id = id).all()
    
    