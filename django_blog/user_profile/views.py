from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, UserProfileUpdateForm, ProfilePictureUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .decorators import not_logged_in_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import User

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