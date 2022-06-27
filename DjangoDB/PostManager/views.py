import os

from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import ProtectedError
from PostManager.database import Database
from PostManager.models import Post
from PostManager.form import PostForm
from PostManager.validators import *
from PostManager.tools import getRequestMethod

from rest_framework.decorators import api_view

db = Database() #creates basic database objects
#connects to database based on variables in system environment variables
db.connect(os.getenv("DB_TYPE"), os.getenv("DB_NAME"), os.getenv("DB_IP"), os.getenv("DB_PORT"), os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"))

#PostManager wrapper class
class PostManagerView:

    @api_view(['GET', 'POST'])
    def index(request):
        match getRequestMethod(request):
            case 'GET':
                return render(request, 'showPosts.html', {'posts': Post.objects.all().order_by('id'), 'count': Post.objects.all().count(), 'prevUrl': request.path})
            case 'POST':
                posts = getPostsFromAPI()
                for post in posts:
                    if (validateUserId(post['userId'])):
                        if (Post.objects.get_or_create(userId=post['userId'], title=post['title'], body=post['body'])):
                            print('[OK] Post created successfully')

            case 'DELETE':
                posts = Post.objects.all()
                for post in posts:
                    try:
                        post.delete()
                    except ProtectedError:
                        print('[ERROR] This post cannot be deleted!')

        return HttpResponseRedirect('/posts')

    @api_view(['GET','POST'])
    def create(request):
        match(getRequestMethod(request)):
            case 'GET':
                form = PostForm()
                if('userId' in request.GET.keys()):
                    form.fields['userId'].initial = request.GET.get('userId')
                    #form.fields['userId'].widget.attrs['disabled'] = 'disabled'
                return render(request,'newPostForm.html', {'form': form, 'prevUrl': request.GET.get('prevUrl', '/posts')}, status=200)
            case 'POST':
                postForm = PostForm(request.POST) #fills post form with data from html form
                postForm.fields['userId'].widget.attrs['disabled'] = False
                if (not postForm.is_valid()):
                    return HttpResponseRedirect('/posts/create')
                data = postForm.cleaned_data
                try:
                    if (Post.objects.get_or_create(userId=data['userId'], title=data['title'], body=data['body'])):
                        print('[OK] Post created successfully')
                except IntegrityError:
                    print('[ERROR] This post cannot be created!')
                return HttpResponseRedirect(request.POST.get('prevUrl', '/posts'))

    @api_view(['GET', 'POST'])
    def show(request, id):
        post = None
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            posts = getPostsFromAPI()
            for p in posts:
                if (p['id'] == int(id)):
                    try:
                        post = Post.objects.create(id=id, userId=p['userId'], title=p['title'], body=p['body'])
                        break
                    except IntegrityError:
                        print('[ERROR] This post cannot be created!')
                        return HttpResponseRedirect('/posts')
            if(post is None):
                print(f'[ERROR] Post with ID {id} was not found in database!')
                return HttpResponseRedirect('/posts')

        except Post.MultipleObjectsReturned:
            return HttpResponseRedirect('/posts')

        match(getRequestMethod(request)):
            case 'GET':
                data = {
                    'userId': post.userId,
                    'title': post.title,
                    'body': post.body
                }
                form = PostForm(initial=data)
                form.fields['userId'].widget = forms.HiddenInput() #prevents from changing userId
                form.fields['userId'].initial = post.userId
                for key in form.fields.keys():
                    form.fields[key].widget.attrs['disabled'] = 'disabled' #disables editing
                return render(request, 'showPost.html', {'id': id, 'form': form, 'prevUrl': request.path}, status=200)
            case 'PUT':
                postForm = PostForm(request.POST)
                if (not postForm.is_valid()):
                    return HttpResponseRedirect('/posts')
                data = postForm.cleaned_data
                post.title = data['title']
                post.body = data['body']
                post.save()
                print('[OK] Post updated successfully')
                return HttpResponseRedirect(request.POST.get('prevUrl', '/posts'))
            case 'DELETE':
                try:
                    if (post.delete()):
                        print('[OK] Post deleted successfully')
                        return HttpResponseRedirect(request.POST.get('prevUrl', '/posts'))
                except ProtectedError:
                    print('[ERROR] This post cannot be deleted!')
                    return HttpResponseRedirect('/posts')

    @api_view(['GET'])
    def edit(request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist or Post.MultipleObjectsReturned:
            return HttpResponseRedirect('/posts')
        data = {
            'title': post.title,
            'body': post.body
        }
        form = PostForm(initial=data) #pre fills form
        form.fields['userId'].widget = forms.HiddenInput() #prevents userId from changing
        form.fields['userId'].initial = post.userId #sets initial userId
        return render(request, 'editPostForm.html', {'form': form, 'id': post.id, 'prevUrl': request.GET['prevUrl']}, status=200)

    @api_view(['GET'])
    def showUserPosts(request, userId):
        try:
            posts = Post.objects.filter(userId=userId).order_by('id')
        except Post.DoesNotExist:
            return HttpResponseRedirect('/posts')
        return render(request, 'showPosts.html', {'posts': posts, 'count': posts.count() ,'prevUrl': request.path, 'userId': userId}, status=200)
