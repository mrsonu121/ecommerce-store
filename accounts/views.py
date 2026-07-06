from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from .forms import RegisterForm, UserUpdateForm


# ================= Register =================
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            messages.success(
                request,
                "Registration Successful"
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


# ================= Login =================
def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(
        request,
        "login.html"
    )


# ================= Logout =================
def logout_user(request):

    logout(request)

    return redirect("home")


# ================= Profile =================
@login_required
def profile(request):

    return render(
        request,
        "profile.html"
    )


# ================= Edit Profile =================
@login_required
def edit_profile(request):

    if request.method == "POST":

        form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile Updated Successfully."
            )

            return redirect("profile")

    else:

        form = UserUpdateForm(
            instance=request.user
        )

    return render(
        request,
        "edit_profile.html",
        {
            "form": form
        }
    )


# ================= Change Password =================
@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password Changed Successfully."
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "change_password.html",
        {
            "form": form
        }
    )