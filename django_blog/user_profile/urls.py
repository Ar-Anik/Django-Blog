from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_user, name="login"),
    path('registration/', registration_user, name="registration"),
    path('logout/', logut_user, name="logout"),
    path('profile/', user_profile, name="profile"),
    path('change_profile_picture/', change_profile_picture, name="change_profile_picture"),
    path('view_user_information/<str:username>/', view_user_information, name="view_user_information"),
    path('follow_or_unfollow/<int:user_id>/',follow_or_unfollow, name='follow_or_unfollow'),
    path('user_notification/', user_notification, name="user_notification"),
    path('mute_and_unmuted/<int:user_id>/', mute_and_unmuted, name='mute_and_unmuted'),
]
