from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Tag, Category, Comment, Reply
from user_profile.models import User
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .forms import TextForm, AddBlogForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.utils.text import slugify
from django.contrib import messages
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
    like_by = blog.likes.all()

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
        "form": form,
        "like_by": like_by
    }

    return render(request, 'blog_post_detail.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def like_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    context = {}
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = blog.likes.all().count()

    else:
        blog.likes.add(request.user)
        context['liked'] = True
        context['like_count'] = blog.likes.all().count()

    return JsonResponse(context, safe=False)

def search_blog(request):
    search_key = request.GET.get('search', None)
    blog_recent_posts = Blog.objects.order_by('-created_date')
    tags = Tag.objects.all()[:6]

    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key)
        ).distinct()

        context = {
            "blogs": blogs,
            "blog_recent_posts": blog_recent_posts,
            "tags": tags
        }

        return render(request, "search.html", context)

    else:
        return redirect('home')

@login_required(login_url='login')
def my_blogs(request):
    data = request.user.blog_user.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 6)

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
        "paginator": paginator
    }

    return render(request, "my_blogs.html", context)


@login_required(login_url='login')
def add_blog(request):
    form = AddBlogForm()

    if request.POST:
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )

                if tag_input.exists():
                    tg = tag_input.first()
                    blog.tags.add(tg)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)

            messages.success(request, "Blog added Successsfully")
            return redirect('blog_detail', slug=blog.slug)

    context = {
        'form': form,
    }

    return render(request, 'add_blog.html', context)

@login_required(login_url='login')
def update_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    form = AddBlogForm(instance=blog)

    if request.POST:
        form = AddBlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            if request.user.pk != blog.user.pk:
                return redirect('home')

            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])

            blog = form.save(commit=False)
            blog.user = user
            blog.category = category

            blog.save()

            for tag in tags:
                tag_exists = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )

                if tag_exists.exists():
                    tg = tag_exists.first()
                    blog.tags.add(tg)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)

            messages.success(request, "Blog Update Successfully")
            return redirect('blog_detail', slug=blog.slug)

    context = {
        'form': form,
        'blog': blog
    }

    return render(request, 'update_blog.html', context)