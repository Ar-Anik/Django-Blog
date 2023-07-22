from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, UserProfileUpdateForm, ProfilePictureUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .decorators import not_logged_in_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import User, Follow
from notification.models import Notification
# Create your views here.

@never_cache
@not_logged_in_required
def login_user(request):
    form = LoginForm()

    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password')
            )

            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Wrong Credentials")

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logut_user(request):
    logout(request)
    return redirect('home')


@never_cache
@not_logged_in_required
def registration_user(request):
    form = UserRegistrationForm()

    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()

            messages.success(request, "Registration Successful")
            return redirect('login')

        # else:
        #     print(form.errors)

    context = {
        'form': form,
    }

    return render(request, 'registration.html', context)

@login_required(login_url='login')
def user_profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)

    if request.POST:
        if request.user.pk != account.pk:
            return redirect('home')

        form = UserProfileUpdateForm(request.POST, instance=account)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Has Been Updated Successfully")
            return redirect('profile')


    context = {
        'account': account,
        'form': form,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def change_profile_picture(request):
    if request.POST:
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['profile_image']
            user = get_object_or_404(User, pk=request.user.pk)
            if request.user.pk != user.pk:
                return redirect('home')

            user.profile_image = image
            user.save()
            messages.success(request, "Profile Image Updated Successfully")

    return redirect('profile')

def view_user_information(request, username):
    account = get_object_or_404(User, username=username)
    following = False
    muted = False

    if request.user.is_authenticated:

        if request.user.id == account.id:
            return redirect('profile')

        followers = account.followers.filter(
            followed_by__id=request.user.id
        )

        if followers.exists():
            following = True

        if following and followers.first().mute:
            muted = True
        else:
            muted = False


    context = {
        "account": account,
        "following": following,
        "muted": muted
    }

    return render(request, 'user_information.html', context)

@login_required(login_url='login')
def follow_or_unfollow(request, user_id):
    followed = get_object_or_404(User, id=user_id)
    followed_by = get_object_or_404(User, id=request.user.id)

    follow, create = Follow.objects.get_or_create(
        followed=followed,
        followed_by=followed_by
    )

    if create:
        followed.followers.add(follow)

    else:
        followed.followers.remove(follow)
        follow.delete()

    return redirect('view_user_information', username=followed.username)

@login_required(login_url='login')
def user_notification(request):
    notifications = Notification.objects.filter(
        user = request.user,
        is_seen = False
    )

    for notification in notifications:
        notification.is_seen = True
        notification.save()

    return render(request, 'notification.html')

@login_required(login_url='login')
def mute_and_unmuted(request, user_id):
    followed = get_object_or_404(User, pk=user_id)
    followed_by = get_object_or_404(User, pk=request.user.id)

    instance = get_object_or_404(Follow, followed=followed, followed_by=followed_by)

    if instance.mute:
        instance.mute = False
        instance.save()

    else:
        instance.mute = True
        instance.save()

    return redirect('view_user_information', username=followed.username)
