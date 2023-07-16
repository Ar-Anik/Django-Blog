from django.urls import path
from .views import home, blogs, category_blogs, tag_blogs, blog_detail, add_reply, like_blog, search_blog, my_blogs, add_blog, update_blog

urlpatterns = [
    path('', home, name="home"),
    path('blogs/', blogs, name="blogs"),
    path('category_blogs/<str:slug>/', category_blogs, name="category_blogs"),
    path('tag_blogs/<str:slug>/', tag_blogs, name="tag_blogs"),
    path('blog_detail/<str:slug>/', blog_detail, name="blog_detail"),
    path('reply_comment/<int:blog_id>/<int:comment_id>/', add_reply, name="reply_comment"),
    path('blog_like/<int:pk>/', like_blog, name="user_like"),
    path('search_blog/', search_blog, name="search_blog"),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('add_blog/', add_blog, name='add_blog'),
    path('update_blog/<str:slug>/', update_blog, name='update_blog'),
]
