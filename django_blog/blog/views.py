from django.shortcuts import render
from .models import Blog, Tag
# Create your views here.

def home(request):
    blog = Blog.objects.order_by('-created_date')
    tags = Tag.objects.all()
    context = {
        "blogs": blog,
        "tags": tags
    }
    return render(request, 'home.html', context)

def blogs(request):
    return render(request, 'blogs.html')
