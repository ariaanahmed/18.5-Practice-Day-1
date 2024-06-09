from django.shortcuts import render, redirect
from .forms import RegisterForm, CustomAuthenticationForm, CustomPasswordForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


def home(request):
    return render(request, "home.html")


# signup
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "signup.html", {"form": form, "type": "Signup"})


# login
def user_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["username"]
            pswd = form.cleaned_data["password"]
            user = authenticate(username=name, password=pswd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("profile")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form, "type": "Login"})


# profile
def profile(request):
    if request.user.is_authenticated:
        # messages.success(request, "Logged in successfully!")
        return render(request, "profile.html", {"user": request.user})
    else:
        return redirect("login")


# logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out!")
    return redirect("home")


# change password
def pass_change(request):
    if request.method == "POST":
        form = CustomPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password updated successfully!")
            return redirect("profile")
    else:
        form = CustomPasswordForm(user=request.user)
    return render(
        request, "pass_change.html", {"form": form, "type": "Change Password"}
    )


# change password2
def pass_change2(request):
    if request.method == "POST":
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password updated successfully!")
            return redirect("profile")
    else:
        form = SetPasswordForm(user=request.user)
    return render(
        request, "pass_change.html", {"form": form, "type": "Change Password"}
    )