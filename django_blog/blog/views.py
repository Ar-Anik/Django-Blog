from django.shortcuts import render, redirect
from .models import Blog, Tag
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
# Create your views here.

def home(request):
    blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.all()
    context = {
        "blogs": blogs,
        "tags": tags
    }
    return render(request, 'home.html', context)

def blogs(request):
    data = Blog.objects.order_by('-created_date')
    tags = Tag.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 4)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
        return redirect('blogs')
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "blog_recent_posts": data,
        "tags": tags,
    }

    return render(request, 'blogs.html', context)

