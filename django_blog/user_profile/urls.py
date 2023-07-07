from django.urls import path
from .views import login, registration

urlpatterns = [
    path('login/', login, name="login"),
    path('registration/', registration, name="registration"),
]
