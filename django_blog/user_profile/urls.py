from django.urls import path
from .views import login_user, registration_user, logut_user

urlpatterns = [
    path('login/', login_user, name="login"),
    path('registration/', registration_user, name="registration"),
    path('logout/', logut_user, name="logout"),
]
