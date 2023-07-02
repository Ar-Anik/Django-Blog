from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Tag, Category, Comment, Reply
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .forms import TextForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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

def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    data = category.blog_category.all()

    tags = Tag.objects.all()

    recent_blog_post = Blog.objects.order_by('-created_date')

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 4)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
        return redirect(request.path)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect(request.path)

    context = {
        "blogs": blogs,
        "tags": tags,
        "recent_blog_post": recent_blog_post
    }

    return render(request, 'category_blogs.html', context)

def tag_blogs(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    data = tag.blog_tag.all()

    tags = Tag.objects.all()[:10]
    recent_blog_post = Blog.objects.order_by('-created_date')[:10]

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 4)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
        return redirect(request.path)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect(request.path)

    context = {
        "blogs": blogs,
        "tags": tags,
        "recent_blog_post": recent_blog_post
    }

    return render(request, 'tag_blogs.html', context)

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id=blog.category.id)
    related_blogs = category.blog_category.all()[:5]
    tags = Tag.objects.all()[:8]

    form = TextForm()

    if request.POST and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                blog=blog,
                text=form.cleaned_data.get('text')
            )
            return redirect('blog_detail', slug=slug)

    context = {
        "blog": blog,
        "related_blogs": related_blogs,
        "tags": tags,
        "form": form
    }

    return render(request, 'blog_post_detail.html', context)

@login_required(login_url='/')
def add_reply(request, blog_id, comment_id):
    blog = Blog.objects.get(id=blog_id)

    if request.POST and request.user.is_authenticated:
        form = TextForm(request.POST)
        comment = get_object_or_404(Comment, id=comment_id)
        if form.is_valid():
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )

            return redirect('blog_detail', slug=blog.slug)

@login_required(login_url='/')
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    context = {}
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = blog.likes.all().count()

    else:
        blog.likes.add(request.user)
        context['liked'] = True
        context['like_count'] = blog.likes.all().count()

    JsonResponse(context, safe=False)
