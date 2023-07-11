from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .decorators import not_logged_in_required
from django.views.decorators.cache import never_cache

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
