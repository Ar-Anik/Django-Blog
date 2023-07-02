from django.db import models
from user_profile.models import User
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Tag(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Blog(models.Model):
    user = models.ForeignKey(User, related_name='blog_user', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='blog_category', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='blog_tag', blank=True)
    likes = models.ManyToManyField(User, related_name='user_like', blank=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(null=True, blank=True)
    banner = models.ImageField(upload_to="blog_banners")
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='blog_comment', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Reply(models.Model):
    user = models.ForeignKey(User, related_name='user_reply', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment_reply', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
