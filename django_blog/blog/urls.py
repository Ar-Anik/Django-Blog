from django.urls import path
from .views import home, blogs

urlpatterns = [
    path('', home, name="home"),
    path('blogs/', blogs, name="blogs"),
]
