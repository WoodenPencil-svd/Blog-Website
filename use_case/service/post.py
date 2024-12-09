from a_posts.models import *
from django.db import transaction
from uuid import UUID


class PostService:
    @transaction.atomic
    def create(self, input: dict, *args, **kwargs):
        tags = input.pop('tags', [])
        post = Post.objects.create(**input)
        post.tags.set(tags)
        return post

    
    @transaction.atomic
    def update(self, id, input: dict):
        id = UUID(str(id))
        post = Post.objects.filter(pk=id).first()
        tags = input.pop('tags', None)
        if tags is not None:
            post.tags.set(tags)
        Post.objects.filter(pk=id).update(**input)
        return post
        
    @transaction.atomic
    def delete(self, id,*args, **kwargs):
        id = UUID(str(id))
        Post.objects.filter(pk=id).delete()