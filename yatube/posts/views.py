from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Group, Post, User
from .forms import PostForm

num_of_posts = 10

def index(request):
    template = 'posts/index.html'
    paginator = Paginator(Post.objects.select_related('group', 'author'), num_of_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    paginator = Paginator(group.posts.all(), num_of_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)

   
def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author__username=username)
    paginator = Paginator(posts, num_of_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
      'page_obj': page_obj,
      'posts' : posts,
      'author': author,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, template, context)

def post_create(request):
    template = 'posts/post_create.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:profile', new_post.author)
        return render(request, template, {'form': form})
    form = PostForm()
    return render(request, template, {'form': form})

def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        if request.user is not post.author:
            return redirect('posts:post_detail', post_id=post.id)
        form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post.id)
    return render(request, 'post_create.html', {'form': form, 'post': post})
