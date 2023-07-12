from django.urls import path
from .views import login_user, registration_user, logut_user, user_profile, change_profile_picture

urlpatterns = [
    path('login/', login_user, name="login"),
    path('registration/', registration_user, name="registration"),
    path('logout/', logut_user, name="logout"),
    path('profile/', user_profile, name="profile"),
    path('change_profile_picture/', change_profile_picture, name="change_profile_picture"),
]
