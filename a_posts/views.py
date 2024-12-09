from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required


def home_view(request, tag = None):
    if tag:
     posts = Post.objects.filter(tags__slug=tag)
     tag = get_object_or_404(Tag,slug=tag)
    else:
     posts = Post.objects.all()
    categories = Tag.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'tag' : tag,
    }
    return render(request, 'a_posts/home.html', context)

@login_required
def post_create_view(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.cleaned_data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')

            find_image = sourcecode.select('img.main-photo')
            image = find_image[0]['src']
            post.image = image

            find_title = sourcecode.select(' h1.meta-field.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            post.author = request.user

            find_artist = sourcecode.select('a.owner-name.truncate')
            artist = find_artist[0].text.strip()
            post.artist = artist

            post.save()
            form.save()
            messages.success(request,'Post created')
            return redirect('home')

    return render(request, 'a_posts/post_create.html', {'form': form})


@login_required
def post_delete_view(request,pk):
    #post = Post.objects.get(id = pk)
    post = get_object_or_404(Post,id=pk,author= request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request,'Post deleted')
        return redirect('home')
    return render(request,'a_posts/post_delete.html',{'post': post })


@login_required
def post_edit_view(request,pk):
    #post = Post.objects.get(id=pk)
    post = get_object_or_404(Post,id=pk,author= request.user)
    form = PostEditForm(instance = post) 
    if request.method == 'POST':
        form = PostEditForm(request.POST,instance = post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post updated')
            return redirect('home')
    context = {
        'post': post, 
        'form' : form
    }
    return render(request,'a_posts/post_edit.html',context)

 
def post_page_view(request,pk):
    # post = Post.objects.get(id = pk )
    post = get_object_or_404(Post,id=pk)
    return render(request,'a_posts/post_page.html',{'post':post})

