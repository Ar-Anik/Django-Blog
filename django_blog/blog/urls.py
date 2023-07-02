from django.urls import path
from .views import home, blogs, category_blogs, tag_blogs, blog_detail, add_reply

urlpatterns = [
    path('', home, name="home"),
    path('blogs/', blogs, name="blogs"),
    path('category_blogs/<str:slug>/', category_blogs, name="category_blogs"),
    path('tag_blogs/<str:slug>/', tag_blogs, name="tag_blogs"),
    path('blog_detail/<str:slug>/', blog_detail, name="blog_detail"),
    path('reply_comment/<int:blog_id>/<int:comment_id>/', add_reply, name="reply_comment"),
]
