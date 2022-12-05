from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Group

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
    paginator = Paginator(group.posts.select_related('author'), num_of_posts)
    page_number = request.Get.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)
